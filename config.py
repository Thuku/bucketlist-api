"""Configration file."""
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """configuration."""

    SQLALCHEMY_DATABASE_URI = 'postgres://bucketlist'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ERROR_404_HELP = False


class TestingConfig(Config):
    """Testing configuration."""

    SQLALCHEMY_DATABASE_URI = ("sqlite:///" + os.path.join(basedir, 'test.db'))
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    DEBUG = False


class DevelopmentConfig(Config):
    """Development configuration."""
    SQLALCHEMY_DATABASE_URI = 'postgres://thuku@localhost:5432/bucketlist'
    DEBUG = True


configuration = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
