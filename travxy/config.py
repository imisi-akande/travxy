from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Development(object):
    """Base config."""
    DEBUG = True
    TESTING = False
    FLASK_ENV = 'development'
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')


class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')

app_config = {
    'development': Development,
    'production': Production,
}