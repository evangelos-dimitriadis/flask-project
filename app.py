from flask import Flask
from views import main
from jinja_helpers import register_jinja_helpers
from api.monetdbd import MONETDBD
from api.monetdb import MONETDB
from api.errors import errors
import logging


def create_app():

    app = Flask(__name__)

    register_jinja_helpers(app)

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    app.register_blueprint(main)

    app.register_blueprint(errors)
    app.register_blueprint(MONETDBD, url_prefix='/api/v1')
    app.register_blueprint(MONETDB, url_prefix='/api/v1')

    return app
