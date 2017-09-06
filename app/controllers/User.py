"""Authentication."""
from flask import Flask, request, make_response, json, jsonify
from flask_restful import reqparse, request, Resource
from app import db, bcrypt
from app.models.Models import User
from app.controllers.login import logged_in


class Register(Resource):
    """Authentication class."""

    def post(self):
        """Registration New user."""
        parser = reqparse.RequestParser()
        parser.add_argument('username',
                            type=str,
                            required=True,
                            help='Username required',
                            location="json")
        parser.add_argument('email',
                            required=True,
                            help='Email required',
                            location="json")
        parser.add_argument('password',
                            required=True,
                            help='Password required',
                            location="json")
        parser.add_argument('confirm_password',
                            required=True,
                            help='Required',
                            location="json")
        arguments = parser.parse_args()

        if arguments['password'] != arguments['confirm_password']:
            responseObject = {
                'status': 'Fail',
                'message': 'Please confirm you password'
            }
            return make_response(jsonify(responseObject), 401)
        elif len(arguments['password']) < 6:
            responseObject = {
                'status': 'Fail',
                'message': 'password should be more than Six characters'
            }
            return make_response(jsonify(responseObject), 400)
        elif len(arguments['username']) < 5:
            responseObject = {
                'status': 'Fail',
                'message': 'Username should be more than Five characters'
            }
            return make_response(jsonify(responseObject), 400)
        elif (arguments['username'].strip()).isalpha() is False:
            responseObject = {
                'status': 'Fail',
                'message': 'Username should not have special spaces/characters'
            }
            return make_response(jsonify(responseObject), 400)
        elif User.query.filter_by(user_name=arguments.get('username')).first():
            responseObject = {
                'status': 'Fail',
                'message': 'Username is already taken'
            }
            return make_response(jsonify(responseObject), 409)

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

    @logged_in
    def get(self, user_id=None, res=None):
        if user_id is not None:
            user = User.query.get(user_id)
            responseObject = {
                'status': 'success',
                'username': user.user_name
                }
        return make_response(jsonify(responseObject), 200)


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, location="json")
        parser.add_argument('password', required=True, location="json")
        arguments = parser.parse_args()
        username = arguments.get('username')

        user = User.query.filter_by(user_name=username).first()
        if not user:
            responseObject = {
                'status': 'Fail',
                'message': 'Username does not exist'
            }
            return make_response(jsonify(responseObject), 401)
        else:
            res = bcrypt.check_password_hash(
                user.password, arguments.get('password'))
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
                return make_response(jsonify(responseObject), 401)
