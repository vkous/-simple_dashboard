import os

class BaseConfig():

   TESTING = False
   DEBUG = False

   STATIC_FOLDER = '/static'
   TEMPLATES_FOLDER = '/templates'
   DATABASE = "database.db"


class DevConfig(BaseConfig):
   def __init__(self): 
      print('***** Environment : Dev')
   FLASK_ENV = 'development'
   DEBUG = True


class ProductionConfig(BaseConfig):
   def __init__(self): 
      print('***** Environment : Production')
   FLASK_ENV = 'production'
   DATABASE = "/var/www/dashboard/dashboard/database.db"


class TestConfig(BaseConfig):
   def __init__(self): 
      print('***** Environment : Test')
   FLASK_ENV = 'development'
   DATABASE = "/var/www/dashboard/dashboard/database.db"
   TESTING = True
   DEBUG = True

