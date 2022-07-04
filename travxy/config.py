import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    """Base config."""
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    FLASK_ENV = os.environ.get("FLASK_ENV")


class ProductionConfig(Config):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_PRODUCTION_DATABASE_URI')

class TestingConfig(Config):
    """
    Test environment configurations
    """
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'test': TestingConfig
}

