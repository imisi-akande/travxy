import configparser
import os
#from os import environ, path
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
print(os.getenv("SQLALCHEMY_DATABASE_URI"), 'are you there')



class Development(object):
    """Base config."""
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    FLASK_ENV = os.environ.get("FLASK_ENV")


class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

developing = Development()
app_config = {
    'development': Development,
    'production': Production,
}
print(Development.JWT_SECRET_KEY, 'talk')
print(app_config['development'], 'show us in config')
