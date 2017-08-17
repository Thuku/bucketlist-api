"""Authentication."""
from flask import Flask, request, make_response, json, jsonify
from flask_restful import reqparse, request, Resource
from app import db, bcrypt
from app.models.Models import User


class Register(Resource):
    """Authentication class."""

    def get(self):
        """Get endtpoint."""
        return {"Authenticate": "Please try again"}

    def post(self):
        """Registration endtpoint."""
        parser = reqparse.RequestParser()
        parser.add_argument('username',
                            type=str,
                            required=True,
                            help='Username required')
        parser.add_argument('email', required=True, help='Email required')
        parser.add_argument('password',
                            required=True, help='Password required')
        parser.add_argument('confirm_password', required=True, help='Required')
        arguments = parser.parse_args(strict=True)

        if arguments['password'] != arguments['confirm_password']:
            responseObject = {
                'status': 'Fail',
                'message': 'Please confirm you password'
            }
            return make_response(jsonify(responseObject))
        elif len(arguments['password']) < 6:
            responseObject = {
                'status': 'Fail',
                'message': 'password should be more than Six characters'
            }
            return make_response(jsonify(responseObject))
        elif len(arguments['username']) < 5:
            responseObject = {
                'status': 'Fail',
                'message': 'Username should be more than Five characters'
            }
            return make_response(jsonify(responseObject))
        elif User.query.filter_by(user_name=arguments.get('username')).first():
            responseObject = {
                'status': 'Fail',
                'message': 'Username is already taken'
            }
            return make_response(jsonify(responseObject))

        else:

            user = User.query.filter_by(email=arguments.get('email')).first()
            if not user:
                user = User(
                    user_name=arguments.get('username'),
                    email=arguments.get('email'),
                    password=arguments.get('password')
                )
                db.session.add(user)
                db.session.commit()

                responseObject = {
                    'status': 'Successful',
                    'message': 'Registration Successful, You can now login into your account',

                }
                return make_response(jsonify(responseObject), 201)

            return make_response(jsonify({
                "message": "Email is taken, please try again"
            }), 409)


class Login(Resource):
    def __init__(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        arguments = parser.parse_args(strict=True)

        user = User.query.filter_by(user_name=arguments.get('username')).first()
        if not user:
            responseObject = {
                'status': 'Fail',
                'message': 'Username does not exist'
            }
            return make_response(jsonify(responseObject))
        else:
            res = bcrypt.check_password_hash(pw_hash=user.password, password=arguments.get('password'))

            if res is True:
                user_id = user.id
                token = user.generate_token(user_id)

                responseObject = {
                    'status': 'success',
                    'message': ' Login successful',
                    'token': str(token)
                }
                return make_response(jsonify(responseObject))
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Wrong password'
                }
                return make_response(jsonify(responseObject))




