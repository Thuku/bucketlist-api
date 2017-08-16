"""Configration file."""


class Config(object):
    """configuration."""

    SQLALCHEMY_DATABASE_URI = 'postgres://bucketlist'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Testing configuration."""

    SQLALCHEMY_DATABASE_URI = 'postgres://thuku:thuku@localhost:5432/test_bucketlist'
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False


class DevelopmentConfig(Config):
    """Development configuration."""
    SQLALCHEMY_DATABASE_URI = 'postgres://thuku:thuku@localhost:5432/bucketlist'
    DEBUG = True


configuration = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}
