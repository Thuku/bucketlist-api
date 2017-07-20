from flask_script import Manager

from app import app

manager = Manager()

if __name__ == '__main__':
    manager.run()