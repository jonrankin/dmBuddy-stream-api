import os


class DatabaseConfig:
    """Base Database Configuration."""
    DATABASE_BASE = os.getenv('DATABASE_URL', 'postgresql://postgres:@localhost/')
    DATABASE_NAME = os.getenv('DATABASE_NAME','dm-buddy')
    DATABASE_URI  = DATABASE_BASE + DATABASE_NAME

class AppConfig:
   """Base Configuration."""
   SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
   DEBUG = False
   BCRYPT_LOG_ROUNDS = 13
   SQLALCHEMY_TRACK_MODIFICATIONS = False
   SQLALCHEMY_DATABASE_URI = DatabaseConfig.DATABASE_URI


class TestingConfig:
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = DatabaseConfig.DATABASE_URI + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
