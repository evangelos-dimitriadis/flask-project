import os
import subprocess
import re
from flask import current_app
from api.errors import InvalidUsage
import psutil
from pathlib import Path
from slugify import slugify
from commands.utils import is_empty


def monetdbd_create(request):
    """
    Accepts dictionary of dbfarm e.g. {'dbfarm': 'mydbfarm'}
    """
    dbfarm = check_db_farm(request)

    execute_command = ['monetdbd', 'create'] + dbfarm
    try:
        result = subprocess.check_output(execute_command, stderr=subprocess.STDOUT, shell=False)
        result = str(result.decode('ascii'))
        result = parse_result(result)
    except subprocess.CalledProcessError as e:
        error_message = str(e.output.decode('ascii')).strip('\n')
        raise InvalidUsage(error_message, status_code=400)
    return result


def monetdbd_start(request):
    """
    Accepts dictionary of dbfarm e.g. {'dbfarm': 'mydbfarm'}
    """
    dbfarm = check_db_farm(request)

    execute_command = ['monetdbd', 'start'] + dbfarm
    try:
        if checkIfProcessRunning('monetdbd'):
            raise InvalidUsage('another monetdbd is already running', status_code=400)
        subprocess.Popen(execute_command, stderr=subprocess.STDOUT, shell=False)
    except subprocess.CalledProcessError as e:
        error_message = str(e.output.decode('ascii')).strip('\n')
        raise InvalidUsage(error_message, status_code=400)


def monetdbd_stop(request):
    """
    Accepts dictionary of dbfarm e.g. {'dbfarm': 'mydbfarm'}
    """
    dbfarm = check_db_farm(request)

    execute_command = ['monetdbd', 'stop'] + dbfarm
    try:
        subprocess.Popen(execute_command, stderr=subprocess.STDOUT, shell=False)
    except subprocess.CalledProcessError as e:
        error_message = str(e.output.decode('ascii')).strip('\n')
        raise InvalidUsage(error_message, status_code=400)


def monetdb_version():
    """
    Returns monetdb version as string e.g. "MonetDB Database Server v11.35.20"
    """
    try:
        result = subprocess.check_output(['monetdbd', 'version'], shell=False).decode('ascii')
        result = str(result).strip('\n')
    except subprocess.CalledProcessError:
        raise InvalidUsage('Internal Server Error', status_code=500)
    return result


def monetdbd_get(request):
    """
    Accepts dictionary of dbfarm, properties
    e.g. {'dbfarm': 'mydbfarm', 'properties': ['hostname', 'status']}
    """
    properties = request.get('properties', None)
    dbfarm = check_db_farm(request)

    # Check if the user input is empty
    if is_empty(properties):
        raise InvalidUsage('Provide at least one property.', status_code=400)

    whitelist = ['all', 'logfile', 'pidfile', 'sockdir', 'port', 'ipv6', 'listenaddr', 'control',
                 'discovery', 'discoveryttl', 'dbfarm', 'exittimeout', 'forward', 'snapshotdir',
                 'snapshotcompression', 'mapisock', 'controlsock', 'status', 'hostname']
    for entry in properties:
        if entry not in whitelist:
            raise InvalidUsage('No such property: ' + entry, status_code=400)

    if 'all' in properties:
        options = ['all']
    else:
        options = [','.join(map(str, properties))]
    execute_command = ['monetdbd', 'get'] + options + dbfarm

    try:
        result = subprocess.check_output(execute_command, stderr=subprocess.STDOUT, shell=False)
        result = str(result.decode('ascii'))
        result = parse_result(result)
    except subprocess.CalledProcessError as e:
        error_message = str(e.output.decode('ascii')).strip('\n')
        raise InvalidUsage(error_message, status_code=400)
    return result


def monetdbd_set(request):
    properties = request.get('properties', None)
    dbfarm = check_db_farm(request)

    # Check if the user input is empty
    if is_empty(properties):
        raise InvalidUsage('Provide at least one property.', status_code=400)

    whitelist = ['all', 'logfile', 'pidfile', 'sockdir', 'port', 'ipv6', 'listenaddr', 'control',
                 'discovery', 'discoveryttl', 'dbfarm', 'exittimeout', 'forward', 'snapshotdir',
                 'snapshotcompression', 'mapisock', 'controlsock', 'status', 'hostname',
                 'passphrase']

    for entry in properties:
        if entry not in whitelist:
            raise InvalidUsage('No such property: ' + entry, status_code=400)

    properties = ['%s=%s' % (key, value) for (key, value) in properties.items()]
    execute_command = ['monetdbd', 'set'] + properties + dbfarm
    current_app.logger.debug(execute_command)

    try:
        result = subprocess.check_output(execute_command, stderr=subprocess.STDOUT, shell=False)
        result = str(result.decode('ascii'))
    except subprocess.CalledProcessError as e:
        error_message = str(e.output.decode('ascii')).strip('\n')
        raise InvalidUsage(error_message, status_code=400)
    return result


def parse_result(result):
    """
    Argument: A monetdbd output, space seperated with property and value
    Returns a dictionary without the headers
    """
    # TODO: Add a blacklist such as [passphrase, ...]
    lines = result.split('\n')
    parsed_dict = {}
    for i in range(1, len(lines) - 1):
        # Remove multiple spaces
        entry = [x for x in re.split("\s{2,}", lines[i]) if x]
        if 'passphrase' in entry[0]:
            continue
        parsed_dict[entry[0]] = entry[1]

    return parsed_dict


def checkIfProcessRunning(processName):
    """
    Check if there is any running process that contains the given name processName
    """
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            current_app.logger.debug('While searching for monetdbd an exception occured: ' + str(e))
            pass

    return False


def check_db_farm(request):
    """
    Sanitize dbfarm user input. Allow the dbfarm to exist on the current path, no subfolders
    """
    if request:
        dbfarm = (request.get('dbfarm', None))
    else:
        raise InvalidUsage('Provide one dbfarm', status_code=400)
    if dbfarm:
        dbfarm = dbfarm.split(',')
    else:
        raise InvalidUsage('Provide one dbfarm', status_code=400)
    if is_empty(dbfarm) or len(dbfarm) != 1:
        raise InvalidUsage('Provide one dbfarm', status_code=400)

    # Remove any unwanted charachters
    dbfarm[0] = slugify(dbfarm[0])
    # Allow dbfarm to be created only in the project's current path. Subject to change.
    basedir = os.getcwd()
    test_path = Path((basedir + '/' + dbfarm[0])).resolve()
    if test_path.parent != Path(basedir).resolve():
        raise InvalidUsage('Do not use a path with dbfarm', status_code=400)

    return dbfarm
