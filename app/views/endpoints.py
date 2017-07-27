from flask import request, Blueprint
from flask_restful import Api


from app.controllers.authentication import Authentication


api_blueprint = Blueprint('bucketlist', __name__)
api = Api(api_blueprint)

api.add_resource(Authentication, '/authentication/login')
