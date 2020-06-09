from flask import jsonify, make_response, Blueprint
import werkzeug

errors = Blueprint('errors', __name__)


class InvalidUsage(Exception):
    """An exception that can take a proper human readable message,
    a status code for the error and some optional payload to give more context for the error."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


# General catch all 404 errorhandler
@errors.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': 'Not Found'}), 404)

# General catch all 400 errorhandler
@errors.app_errorhandler(400)
def bad_request_e(error):
    return make_response(jsonify({'message': 'Bad Request'}), 400)


@errors.app_errorhandler(werkzeug.exceptions.HTTPException)
def handle_exception(error):
    """Return JSON instead of HTML for HTTP errors."""
    return make_response(jsonify({'message': error.description}), 400)

# General catch all 500 errorhandler
@errors.app_errorhandler(500)
def server_error(error):
    return make_response(jsonify({'message': 'Internal Server Error'}), 500)

# A generic errorhandler that can pass custom messages if we catch errors
@errors.app_errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
