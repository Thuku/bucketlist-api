import jwt
import datetime
import os
from flask import jsonify, make_response, request
from functools import wraps

from app import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now,
                           onupdate=datetime.datetime.now),
    buckets = db.relationship("Bucket")

    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = self.hash_password(password)

    def hash_password(self, password):
        return bcrypt.generate_password_hash(password, 12).decode("utf-8")

    def generate_token(self, id):
        """Generate authentication token."""
        payload = {
            'exp': datetime.datetime.now() + datetime.timedelta(seconds=90),
            'iat': datetime.datetime.now(),
            'sub': id
        }
        return jwt.encode(
            payload,
            os.getenv('SECRET_KEY'),
            algorithm='HS256'
        )

class Bucket(db.Model):
    __tablename__ = 'buckets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100))
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(100), default="Inprogress")
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now,
                           onupdate=datetime.datetime.now)
    activities = db.relationship(
        "Activity", cascade="all, delete", backref="buckets")

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return '<name %s>' % (self.name)


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    bucket_id = db.Column(db.Integer, db.ForeignKey('buckets.id'))
    name = db.Column(db.String(100))
    status = db.Column(db.String(100), default="Inprogress")
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now,
                           onupdate=datetime.datetime.now)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<name %s>' % (self.name)


def logged_in(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            payload = jwt.decode(token, os.getenv('SECRET_KEY'))
            user_id = payload['sub']
            user = User.query.get(user_id)
            if user:
                responseObject = {
                    'staus': 'sucess',
                    'message': 'Login successful'
                }
                new_kwargs = {
                    'res': responseObject,
                    'user_id': user.id
                }
                kwargs.update(new_kwargs)
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User not found'
                }
                new_kwargs = {
                    'res': responseObject,
                    'user_id': None
                }
                kwargs.update(new_kwargs)
        except jwt.ExpiredSignatureError:
            responseObject = {
                'status': 'Fail',
                'message': 'Token expired please login'
            }
            return make_response(jsonify(responseObject))
        except jwt.InvalidTokenError:
            responseObject = {
                'status': 'fail',
                'message': 'Invalid token, please log in'
            }
            return make_response(jsonify(responseObject))
        return func(*args, **kwargs)
    return decorator
