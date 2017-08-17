import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db

environment = os.getenv('ENV') or 'development'
app = create_app(config_name=environment)

migrate = Migrate(app, db)
manager = Manager(app)


@manager.command
def createdb():
    db.create_all()
    print("database created successfully")


@manager.command
def dropdb():
    db.drop_all()


manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
