#general imports
import datetime
import os
from dotenv import load_dotenv

from flask import Flask
#from flask import current_app as app
import logging
from logging.handlers import RotatingFileHandler


from dashboard.model import *


load_dotenv()
import dashboard.config


def create_app(test_config=None):
    app = Flask(__name__)

    #LOGS
    handler = RotatingFileHandler('dashboard.log', maxBytes=10000, backupCount=0)
    logging_formatter = logging.Formatter("%(asctime)s; %(levelname)s; %(message)s",
                              "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(logging_formatter)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.info('======================= START ======================= ')
    app.logger.info(f'Starting app in {config.APP_ENV} environment')

    #CONFIG
    app.config.from_object('dashboard.config')
    app.config.update(
        SECRET_KEY=os.environ.get('FLASK_SECRET')
        )
    # ensure the instance folder exists
    try:
        app.logger.info('Create instance path if doesn\'t exist')
        os.makedirs(app.instance_path)
    except OSError:
        app.logger.info('instance path already exists')
        pass
    app.logger.info('Configurate flask_app attributes')
    app.permanent_session_lifetime = datetime.timedelta(days=365)


    with app.app_context():
        #initialisation database (first execution)
        if not os.path.exists(app.config['DATABASE']):
            db.init_db()
        # GET ROUTES
        from . import routes
    return app
