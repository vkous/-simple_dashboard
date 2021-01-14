import os

class BaseConfig():

   TESTING = False
   DEBUG = False

   STATIC_FOLDER = '/static'
   TEMPLATES_FOLDER = '/templates'
   DATABASE = "database.db"


class DevConfig(BaseConfig):
   FLASK_ENV = 'development'
   DEBUG = True


class ProductionConfig(BaseConfig):
   FLASK_ENV = 'production'
   DATABASE = "/var/www/dashboard/dashboard/database.db"


class TestConfig(BaseConfig):
   FLASK_ENV = 'development'
   DATABASE = "/var/www/dashboard/dashboard/database.db"
   TESTING = True
   DEBUG = True

