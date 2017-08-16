"""App initialization file."""
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from config import configuration
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


from app.models import Models
from app.views.endpoints import api_blueprint


def create_app(environment):
    """Create application."""
    app = FlaskAPI(__name__)
    app.config.from_object(configuration[environment])
    db.init_app(app)
    app.register_blueprint(api_blueprint)
    return app
