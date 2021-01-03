#general imports
import datetime
import os
from dotenv import load_dotenv

from flask import Flask
from flask import current_app as app
import logging
from logging.handlers import RotatingFileHandler


from dashboard.model import *

load_dotenv()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    handler = RotatingFileHandler('dashboard.log', maxBytes=10000, backupCount=0)

    logging_formatter = logging.Formatter("%(asctime)s; %(levelname)s; %(message)s",
                              "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(logging_formatter)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.info('======================= START ======================= ')
    
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        DATABASE=os.path.join(app.instance_path, 'dashboard_db.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.logger.info('Load config.py')
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.logger.info('Load test config if passed in')
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        app.logger.info('Create instance path if doesn\'t exist')
        os.makedirs(app.instance_path)
    except OSError:
        app.logger.info('instance path already exists')
        pass
    app.logger.info('Configurate flask_app attributes')
    app.config['FLASK_DEBUG'] = True
    app.config['STATIC_FOLDER'] = '/static'
    app.config['TEMPLATES_FOLDER'] = '/templates'
    app.config['DATABASE'] = 'database.db'
    app.permanent_session_lifetime = datetime.timedelta(days=365)


    with app.app_context():
        #initialisation database (first execution)
        if not os.path.exists(app.config['DATABASE']):
            db.init_db()
        #from . import routes
        from . import _test
    return app
