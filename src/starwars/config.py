import logging
import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    LOGS_LEVEL = os.environ.get('LOGS_LEVEL', 'INFO')
    DEPLOY_ENV = os.environ.get('DEPLOY_ENV', 'Development')


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    LOGS_LEVEL = logging.CRITICAL
    MONGO_URI = "mongodb://server.test.com"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/api_starwars')


class ProductionConfig(BaseConfig):
    LOGS_LEVEL = os.environ.get('LOGS_LEVEL', 'INFO')
