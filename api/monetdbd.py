from flask import jsonify, make_response, Blueprint, request, current_app
from commands.monetdbd import (monetdbd_create, monetdbd_start, monetdbd_stop, monetdb_version,
                               monetdbd_get, monetdbd_set)

MONETDBD = Blueprint('monetdbd', __name__)


@MONETDBD.route('/monetdbd/help', methods=['GET'])
def monetdbd_help_api():
    command = request.args.get('command', None)
    if command is None:
        return jsonify({'usage': '/api/v1/monetdbd/[ command ]/[ command-options ]',
                        'description': 'Command is one of: '
                        'create, start, stop, get, version or help. '
                        'Use the /api/v1/monetdbd/help/?command=[ command ] to get help for a '
                        'particularesultresultr command. The dbfarm to operate on must always be '
                        'given to monetdbd explicitly.'})
    else:
        command_sanitized = command.strip()
    accepted_commands = ['create', 'start', 'stop', 'get']
    if command_sanitized not in accepted_commands:
        # Return what monetdbd help would print in case of wrong user input along with status code.
        return jsonify({'usage': '/api/v1/monetdbd/[ command ]/[ command-options ]',
                        'description': 'Command is one of: '
                        'create, start, stop, get, version or help. '
                        'Use the /api/v1/monetdbd/help/?command=[ command ] to get help '
                        'for a particular command. '
                        'The dbfarm to operate on must always be given to '
                        'monetdbd explicitly.'}), 400
    elif command_sanitized == accepted_commands[0]:
        return jsonify({'usage': '/api/v1/monetdbd/create/',
                        'description': 'Initialises a new dbfarm for a MonetDB Server. '
                        'dbfarm must be a path in the filesystem where a directory can be '
                        'created, or a directory that is writable that already exists.'})
    elif command_sanitized == accepted_commands[1]:
        return jsonify({'usage': '/api/v1/monetdbd/start/',
                        'description': 'Starts the monetdbd deamon for the given dbfarm.'})
    elif command_sanitized == accepted_commands[2]:
        return jsonify({'usage': '/api/v1/monetdbd/stop/',
                        'description': 'Stops a running monetdbd deamon for the given dbfarm.'})
    elif command_sanitized == accepted_commands[3]:
        return jsonify({'usage': '/api/v1/monetdbd/get/',
                        'description': ' Gets value for property for the given dbfarm, or '
                        'retrieves all properties.'})
    elif command_sanitized == accepted_commands[4]:
        return jsonify({'usage': '/api/v1/monetdbd/version/',
                        'description': 'Returns the MonetDB Database Server version.'})
    else:
        make_response(jsonify({'message': 'Not found'}), 404)


@MONETDBD.route('/monetdbd/create', methods=['POST'])
def monetdbd_create_api():
    monetdbd_create(request.get_json())
    return jsonify({'message': 'success'})


@MONETDBD.route('/monetdbd/start', methods=['POST'])
def monetdbd_start_api():
    monetdbd_start(request.get_json())
    return jsonify({'message': 'success'})


@MONETDBD.route('/monetdbd/stop', methods=['POST'])
def monetdbd_stop_api():
    result = monetdbd_stop(request.get_json())
    return jsonify(result)


@MONETDBD.route('/monetdbd/set', methods=['POST'])
def monetdbd_set_api():
    result = monetdbd_set(request.get_json())
    return jsonify(result)


@MONETDBD.route('/monetdbd/get', methods=['GET'])
def monetdbd_get_api():
    dict = {}
    properties = request.args.get("properties", None)
    if properties:
        dict['properties'] = properties.split(',')
    else:
        dict['properties'] = []
    dict['dbfarm'] = request.args.get('dbfarm', None)
    result = monetdbd_get(dict)
    return jsonify(result)


@MONETDBD.route('/monetdbd/version', methods=['GET'])
def monetdbd_version_api():
    result = monetdb_version()
    return jsonify({'version': result})
