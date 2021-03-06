from importlib import import_module
import locale
import os

#import stuybulletin as app_root
from blueprints import all_blueprints
from extensions import mail, db

import core.authentication

from flask import Flask

APP_ROOT_FOLDER = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_FOLDER = os.path.join(APP_ROOT_FOLDER, 'templates')
STATIC_FOLDER = os.path.join(APP_ROOT_FOLDER, 'static')

def get_config(config_class_string):
    """ Load the Flask config from a class.

    :param config_class_string: The name of the config class to use (See :class:`stuybulletin.config`)
    :type config_class_string: str
    :returns: Config object -- see :class:`stuybulletin.config`"""
    config_module, config_class = config_class_string.rsplit('.', 1)

    config_class_object = getattr(import_module(config_module), config_class)
    config_obj = config_class_object()

    return config_obj

def create_app(config_obj):
    """ Flask application factory.  Inializes and returns the Flask application.

    This is where blueprints are registered.
    
    :param config_obj: The configuration object to use to initialize the flask application.
    :type config_obj: See :class:`stuybulletin.config`
    :returns: The initialized Flask application.
    """

    # Basic Flask initialization, loads the config from the config obj
    app = Flask(__name__, template_folder = TEMPLATE_FOLDER, static_folder = STATIC_FOLDER)
    config_dict = dict([(k, getattr(config_obj, k)) for k in dir(config_obj) if not k.startswith('_')])
    app.config.update(config_dict)

    # Setups blueprints
    for blueprint in all_blueprints:
        import_module(blueprint.import_name)
        app.register_blueprint(blueprint)

    # Initializes helpers (like mail, celery, etc)
    mail.init_app(app)
    db.init_app(app)

    # Activates the middleware
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    with app.app_context():
        import_module('stuybulletin.middleware')

    # Returns the app instance
    return app
