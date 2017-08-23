from flask_api import FlaskAPI

from config import app_config


def create_app(config_name):
    """this method will initialise the flask API instance """
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    return app
