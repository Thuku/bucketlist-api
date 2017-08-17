from flask import request, Blueprint
from flask_restful import Api


from app.controllers.User import Register, Login
from app.controllers.Bucket import BucketsResource, BucketResource
from app.controllers.Activity import ActivitiesResource, ActivityResource


api_blueprint = Blueprint('bucketlist', __name__)
api = Api(api_blueprint)

api.add_resource(Register, '/authentication/register')
api.add_resource(Login, '/authentication/login')

api.add_resource(BucketsResource, '/bucket')
api.add_resource(BucketResource, '/bucket/<int:bucket_id>')

api.add_resource(ActivitiesResource, '/bucket/<int:bucketlist_id>/items')
api.add_resource(ActivityResource, '/bucket/<int:bucketlist_id>/item/<int:item_id>')

