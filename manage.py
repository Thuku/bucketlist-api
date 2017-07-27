from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db
app = create_app("development")

migrate = Migrate(app, db)
manager = Manager(app)


@manager.command
def createdb():
    db.create_all()
    print(db)
    print("Migrating")


@manager.command
def dropdb():
    db.drop_all()


manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
