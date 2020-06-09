import subprocess
from api.errors import InvalidUsage
from slugify import slugify
from flask import current_app
from models.status import serialize_status, serialize_status_long
from models.request_model import validate_model, validate_get_model
from models.properties import serialize_monetdb_get
from commands.utils import is_empty


def monetdb_kill(request):
    request_model = validate_model(request)
    return monetdb_generic_command(request_model, 'kill', allowed_arguments=['all'])


def monetdb_status(request):
    request_model = validate_model(request)
    execute_command = ['monetdb']
    # Pass the options to the execute_command
    execute_command.extend(options_get_request(request_model))
    execute_command.append('status')
    # Pass the arguments to the execute_command
    execute_command.extend(arguments_get_request(request_model,
                                                 'status', allowed_arguments=['long']))

    databases = check_db_name(request_model, allow_empty=True)
    if databases:
        execute_command.extend(databases)

    try:
        result = subprocess.check_output(execute_command, stderr=subprocess.STDOUT, shell=False)
        result = str(result.decode('ascii'))
    except subprocess.CalledProcessError as e:
        error_message = str(e.output.decode('ascii')).replace('\r', ' ').replace('\n', ' ')
        raise InvalidUsage(error_message, status_code=400)

    if "-l" in execute_command:
        result = serialize_status_long(result)
    else:
        result = serialize_status(result)

    return result['status']


def monetdb_start(request):
    request_model = validate_model(request)
    return monetdb_generic_command(request_model, 'start', allowed_arguments=['all'])


def monetdb_stop(request):
    request_model = validate_model(request)
    return monetdb_generic_command(request_model, 'stop', allowed_arguments=['all'])


def monetdb_generic_command(request_model, command, allowed_arguments=[]):

    execute_command = ['monetdb']
    # Pass the options to the execute_command
    execute_command.extend(options_get_request(request_model))

    execute_command.append(command)

    # Pass the arguments to the execute_command
    execute_command.extend(arguments_get_request(request_model, command, allowed_arguments))
    if '-a' not in execute_command:
        database = check_db_name(request_model)
        execute_command += database

    try:
        result = subprocess.check_output(execute_command, stderr=subprocess.STDOUT, shell=False)
        result = str(result.decode('ascii')).replace('\r', ' ').replace('\n', ' ')
    except subprocess.CalledProcessError as e:
        error_message = str(e.output.decode('ascii')).replace('\r', ' ').replace('\n', ' ')
        raise InvalidUsage(error_message, status_code=400)

    return result


def monetdb_create(request):
    request_model = validate_model(request)
    return monetdb_generic_command(request_model, 'create', allowed_arguments=['pattern', 'pass'])


def monetdb_destroy(request):
    request_model = validate_model(request)
    # -f flag is mandatory in destroy
    request_model['arguments']['force'] = True
    return monetdb_generic_command(request_model, 'destroy', allowed_arguments=['force'])


def monetdb_release(request):
    request_model = validate_model(request)
    return monetdb_generic_command(request_model, 'release')


def monetdb_lock(request):
    request_model = validate_model(request)
    return monetdb_generic_command(request_model, 'lock')


def monetdb_version():
    try:
        result = subprocess.check_output(['monetdb', 'version'], stderr=subprocess.STDOUT,
                                         shell=False)
        result = str(result.decode('ascii')).strip('\n')
    except subprocess.CalledProcessError as e:
        error_message = str(e.output.decode('ascii')).strip('\n')
        raise InvalidUsage(error_message, status_code=400)

    return result


def monetdb_get(request):
    """
    Example of input:
    {'options': {'port': '50000'}, 'databases': ['mydb'], 'properties': ['mclients', 'type']}
    """
    request_model = validate_get_model(request)
    execute_command = ['monetdb']
    # Pass the options to the execute_command
    execute_command.extend(options_get_request(request_model))

    execute_command.append('get')
    properties = request_model.get('properties', None)
    # Properties should be a string in the monetdb execute_command
    properties = ','.join(properties)
    # Check if the user input is empty
    if is_empty(properties):
        raise InvalidUsage('Provide at least one property.', status_code=400)

    if 'all' in properties:
        execute_command.append('all')
    else:
        execute_command.append(properties)
    # Get all without db returns everything, while get all db will return all the properties for
    # the given database
    database = check_db_name(request_model, allow_empty=True)
    execute_command += database

    try:
        result = subprocess.check_output(execute_command, stderr=subprocess.STDOUT, shell=False)
        result = str(result.decode('ascii'))
    except subprocess.CalledProcessError as e:
        error_message = str(e.output.decode('ascii')).replace('\r', ' ').replace('\n', ' ')
        raise InvalidUsage(error_message, status_code=400)

    result = serialize_monetdb_get(result)

    return result


def monetdb_set(request):
    request_model = validate_model(request)
    execute_command = ['monetdb']
    # Pass the options to the execute_command
    execute_command.extend(options_get_request(request_model))

    execute_command.append('set')

    # Properties should be a string (property=value) in the monetdb execute_command
    properties = properties_get_request(request_model)
    execute_command.append('property_holder')

    database = check_db_name(request_model)
    execute_command += database

    for entry in properties:
        # For each entry replace the 'property_holder' with a property
        execute_command[-2] = entry
        try:
            result = subprocess.check_output(execute_command, stderr=subprocess.STDOUT, shell=False)
            result = str(result.decode('ascii'))
        except subprocess.CalledProcessError as e:
            error_message = str(e.output.decode('ascii')).replace('\r', ' ').replace('\n', ' ')
            raise InvalidUsage(error_message, status_code=400)

    return result


def check_db_name(request_model, allow_empty=False):
    """
    Sanitize database user input. Allow multiple databases.
    """
    database = None
    if request_model:
        database = request_model.get('databases', None)
    if database is None and allow_empty:
        return None
    if is_empty(database) and allow_empty is False:
        raise InvalidUsage('Provide at least one database', status_code=400)
    elif isinstance(database, list):
        if not all(isinstance(entry, str) for entry in database):
            raise InvalidUsage('List of databases must be in string format', status_code=400)
    else:
        raise InvalidUsage('Provide a database as a list of strings: {"databases": ["<database>"]}',
                           status_code=400)

    # Remove any unwanted charachters
    database = [slugify(entry) for entry in database]

    return database


def options_get_request(request):
    options_list = []
    options = request.get('options', None)
    if options is None:
        return options_list

    host = (options.get('host', None))
    password = (options.get('password', None))
    port = str((options.get('port', None)))

    if host:
        options_list += ['-h', host]
    if password:
        options_list += ['-P', password]
    if port:
        options_list += ['-p', port]

    return options_list


def arguments_get_request(request, command, allowed_arguments):

    arguments_list = []
    arguments = request.get('arguments', None)
    if arguments is None:
        return arguments_list

    for key, value in arguments.items():
        if key not in allowed_arguments:
            raise InvalidUsage('Unknown argument "{}" for endpoint "{}"'.format(str(key), command),
                               status_code=400)

    all = arguments.get('all', None)
    long = arguments.get('long', None)
    password = arguments.get('pass', None)
    force = arguments.get('force', None)

    if all and all is True:
        arguments_list += ['-a']
    if long and long is True:
        arguments_list += ['-l']
    if force and force is True:
        arguments_list += ['-f']
    if password:
        arguments_list += ['-p', password]

    return arguments_list


def properties_get_request(request):
    properties = request.get('properties', None)
    # Check if the user input is empty
    if is_empty(properties):
        raise InvalidUsage('Provide at least one property.', status_code=400)

    properties = ['%s=%s' % (key, value) for (key, value) in properties.items()]

    return properties
