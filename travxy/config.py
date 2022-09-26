import os
from dotenv import load_dotenv
from sqlalchemy.engine.url import URL

basedir = os.path.abspath(os.path.dirname(__file__))
env_setting = load_dotenv(os.path.join(basedir, '.env'))


def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

def create_db_url(user, pw, host, port, db):
    url = URL.create(drivername="postgresql+psycopg2", username=user, password=pw,
                        host=host, port=port, database=db)
    return url

# import .env variables for DB connection
def get_env_db_url(env_setting):
    if env_setting == "development":
        POSTGRES_USER = get_env_variable("DEV_POSTGRES_USER")
        POSTGRES_PW = get_env_variable("DEV_POSTGRES_PW")
        POSTGRES_HOST = get_env_variable("DEV_POSTGRES_HOST")
        POSTGRES_PORT = get_env_variable("DEV_POSTGRES_PORT")
        POSTGRES_DB = get_env_variable("DEV_POSTGRES_DB")
    elif env_setting == "testing":
        POSTGRES_USER = get_env_variable("TESTING_POSTGRES_USER")
        POSTGRES_PW = get_env_variable("TESTING_POSTGRES_PW")
        POSTGRES_HOST = get_env_variable("TESTING_POSTGRES_HOST")
        POSTGRES_PORT = get_env_variable("TESTING_POSTGRES_PORT")
        POSTGRES_DB = get_env_variable("TESTING_POSTGRES_DB")
    elif env_setting == "production":
        POSTGRES_USER = get_env_variable("PROD_POSTGRES_USER")
        POSTGRES_PW = get_env_variable("PROD_POSTGRES_PW")
        POSTGRES_HOST = get_env_variable("PROD_POSTGRES_HOST")
        POSTGRES_PORT = get_env_variable("PROD_POSTGRES_PORT")
        POSTGRES_DB = get_env_variable("PROD_POSTGRES_DB")

    return create_db_url(POSTGRES_USER, POSTGRES_PW, POSTGRES_HOST,
                            POSTGRES_PORT, POSTGRES_DB)

# DB URLS for each Environment
DEV_DB_URL = get_env_db_url("development")
TESTING_DB_URL = get_env_db_url("testing")
PROD_DB_URL = get_env_db_url("production")

class Config(object):
    """Base config."""
    SQLALCHEMY_DATABASE_URI = DEV_DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_ENV = os.environ.get("FLASK_ENV")

class TestingConfig(Config):
    """
    Test environment configurations
    """
    SQLALCHEMY_DATABASE_URI = TESTING_DB_URL
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """
    Production environment configurations
    """
    SQLALCHEMY_DATABASE_URI = PROD_DB_URL
    DEBUG = False
    TESTING = False
