# project/server/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))
database_name = 'transfuzol'

if 'RDS_DB_NAME' in os.environ:
    DB_NAME = "database1"
    DB_USER = os.environ['RDS_USERNAME']
    DB_PASSWORD = os.environ['RDS_PASSWORD']
    DB_HOST = os.environ['RDS_HOSTNAME']
    DB_PORT = os.environ['RDS_PORT']
else:
    DB_NAME = 'transfuzol'
    DB_USER = 'postgres'
    DB_PASSWORD = 'barister'
    DB_HOST = 'localhost'
    DB_PORT = '5432'


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + DB_PORT + '/' + DB_NAME

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
