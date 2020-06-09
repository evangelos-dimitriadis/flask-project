from flask import jsonify, Blueprint, request, current_app
from api.errors import InvalidUsage
from commands.monetdb import (monetdb_stop, monetdb_start, monetdb_status, monetdb_kill,
                              monetdb_create, monetdb_destroy, monetdb_release, monetdb_lock,
                              monetdb_version, monetdb_get, monetdb_set)


MONETDB = Blueprint('monetdb', __name__)


@MONETDB.route('/monetdb/help', methods=['GET'])
def monetdb_help_api():
    command = request.args.get('command', None)
    if command is None:
        return jsonify({'usage': '/api/v1/monetdb/[ command ]/[ command-options ]',
                        'description': 'Command is one of: '
                        'create, destroy, lock, release,'
                        'status, start, stop, kill,'
                        'profilerstart, profilerstop,'
                        'snapshot,'
                        'set, get, inherit,'
                        'discover, help or version. '
                        'Options can be: '
                        ' quiet -- suppress status output'
                        ' host --  hostname to contact (remote merovingian)'
                        ' port -- port to contact'
                        ' pass -- password to use to login at remote merovingian. '
                        'Use the /api/v1/monetdb/help/?command=[ command ] to get help for a '
                        'particular command.'})
    else:
        command_sanitized = command.strip()

    accepted_commands = {
        'create': jsonify({'usage': '/api/v1/monetdb/create/',
                           'description': 'Initialises a new database or multiplexfunnel in the '
                           'MonetDB Server. A database created with this command makes it '
                           'available for use, however in maintenance mode (see monetdb lock). '
                           'Options: '
                           'pattern create a multiplex funnel for pattern. '
                           'pass create database with given password for database user.'}),
        'start': jsonify({'usage': '/api/v1/monetdb/start/',
                          'description': 'Starts the given database, if the MonetDB Database Server'
                          'is running. '
                          'Options:'
                          'all start all known databases'}),
        'stop': jsonify({'usage': '/api/v1/monetdb/stop/',
                         'description': 'Stops the given database, if the MonetDB Database Server'
                         'is running. '
                         'Options:'
                         '-a  start all known databases'}),
        'get': jsonify({'usage': '/api/v1/monetdb/get/',
                        'description': ' Gets value for property for the given database, or '
                        'retrieves all properties for the given database.'}),
        'version': jsonify({'usage': '/api/v1/monetdb/version/',
                            'description': 'Returns the version of this monetdb utility.'})
    }

    return accepted_commands.get(command_sanitized,
                                 (jsonify({'usage':
                                           '/api/v1/monetdb/[ command ]/[ command-options ]',
                                           'description': 'Command is one of: '
                                           'create, destroy, lock, release, '
                                           'status, start, stop, kill, '
                                           'profilerstart, profilerstop, '
                                           'snapshot, '
                                           'set, get, inherit, '
                                           'discover, help or version. '
                                           'Options can be: '
                                           'host --  hostname to contact (remote merovingian) '
                                           'port -- port to contact '
                                           'pass -- password to use to login at remote merovingian.'
                                           ' Use the /api/v1/monetdb/help/?command=[ command ] '
                                           'to get help '
                                           'for a particular command.'}), 400))


@MONETDB.route('/monetdb/stop', methods=['POST'])
def monetdb_stop_api():
    """Stops the given database, if the MonetDB Database Server is running.
    Example of data passed to POST request:
    {"dbfarm":"dbfarm", "databases": ["mydb, mydb2, ..."],
    "options": {"host": "127.0.0.1", "password": "123", "port": "50000"},
    "arguments": {"all": false}}
    """
    result = monetdb_stop(request.get_json())
    return jsonify({'message': result})


@MONETDB.route('/monetdb/start', methods=['POST'])
def monetdb_start_api():
    """Starts the given database, if the MonetDB Database Server is running.
    Example of data passed to POST request:
    {"dbfarm":"dbfarm", "databases": ["mydb, mydb2, ..."],
    "options": {"host": "127.0.0.1", "password": "123", "port": "50000"},
    "arguments": {"all": false}}
    """
    result = monetdb_start(request.get_json())
    return jsonify({'message': result})


@MONETDB.route('/monetdb/status', methods=['GET'])
def monetdb_status_api():
    """
    Shows the state of all databases.
    Example of data passed to GET request:
    .../api/v1/monetdb/status?long=true&hostname=127.0.0.1&password=123&port=50000
    """
    formated_dict = format_dict(request.args.to_dict())
    result = monetdb_status(formated_dict)
    return jsonify(result)


@MONETDB.route('/monetdb/kill', methods=['POST'])
def monetdb_kill_api():
    """Kills the given database, if the MonetDB Database Server is running.
    Example of data passed to POST request:
    {"dbfarm":"dbfarm", "databases": ["mydb, mydb2, ..."],
    "options": {"host": "127.0.0.1", "password": "123", "port": "50000"},
    "arguments": {"all": false}}
    """
    result = monetdb_kill(request.get_json())
    return jsonify({'message': result})


@MONETDB.route('/monetdb/create', methods=['POST'])
def monetdb_create_api():
    """Creates the given database, if the MonetDB Database Server is running.
    Example of data passed to POST request:
    {"dbfarm":"dbfarm", "databases": ["mydb, mydb2, ..."],
    "options": {"host": "127.0.0.1", "password": "123", "port": "50000"},
    "arguments": {"pass": "123"}}
    """
    result = monetdb_create(request.get_json())
    return jsonify({'message': result})


@MONETDB.route('/monetdb/destroy', methods=['DELETE'])
def monetdb_destroy_api():
    """destroys the given database, if the MonetDB Database Server is running.
    Example of data passed to POST request:
    {"dbfarm":"dbfarm", "databases": ["mydb, mydb2, ..."],
    "options": {"host": "127.0.0.1", "password": "123", "port": "50000"},
    "arguments": {}}
    """
    result = monetdb_destroy(request.get_json())
    return jsonify({'message': result})


@MONETDB.route('/monetdb/release', methods=['POST'])
def monetdb_release_api():
    """Brings back a database from maintenance mode.
    Example of data passed to POST request:
    '{"databases": ["mydb", "mydb2"], "options": {"port": 50000}, "arguments": {}}'
    """
    result = monetdb_release(request.get_json())
    return jsonify({'message': result})


@MONETDB.route('/monetdb/lock', methods=['POST'])
def monetdb_lock_api():
    """Puts the given database in maintenance mode.
    Example of data passed to POST request:
    '{"databases": ["mydb", "mydb2"], "options": {"port": 50000}, "arguments": {}}'
    """
    result = monetdb_lock(request.get_json())
    return jsonify({'message': result})


@MONETDB.route('/monetdb/version', methods=['GET'])
def monetdb_version_api():
    """Prints the version of this monetdb utility."""
    result = monetdb_version()
    return jsonify({'message': result})


@MONETDB.route('/monetdb/get', methods=['GET'])
def monetdb_get_api():
    """Prints the version of this monetdb utility."""
    formated_dict = format_dict(request.args.to_dict(), rest_keys='properties')
    result = monetdb_get(formated_dict)
    return jsonify(result)


@MONETDB.route('/monetdb/set', methods=['POST'])
def monetdb_set_api():
    """Prints the version of this monetdb utility."""
    result = monetdb_set(request.get_json())
    return jsonify(result)


def format_dict(request_args, rest_keys='arguments'):
    request_dict = {}
    request_dict['options'] = {}
    request_dict['arguments'] = {}
    request_dict['databases'] = []

    for key, value in request_args.items():
        if key == 'databases':
            request_dict['databases'] = request_args.get('databases').split(',')
        elif key == 'host':
            request_dict['options']['host'] = value
        elif key == 'port':
            request_dict['options']['port'] = value
        elif key == 'password':
            request_dict['options']['password'] = value
        # TODO: An extra check would be to have a list of possible arguments
        elif key == 'arguments':
            request_dict['arguments'][key] = value
        elif key == 'properties':
            request_dict['properties'] = request_args.get('properties').split(',')
        else:
            raise InvalidUsage('Unknown argument: {}'.format(key), status_code=404)

    return request_dict
