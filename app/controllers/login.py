import jwt
import os
from flask import jsonify, make_response, request
from functools import wraps
from app.models.Models import User

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
            return make_response(jsonify(responseObject),401)
        except jwt.InvalidTokenError:
            responseObject = {
                'status': 'fail',
                'message': 'Invalid token, please log in'
            }
            return make_response(jsonify(responseObject))
        return func(*args, **kwargs)
    return decorator
