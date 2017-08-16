"""Authentication."""
from flask import Flask, request, make_response, json, jsonify
from flask_restful import reqparse, request, Resource
from app import  db
from app.models.Models import User, Bucket, Activity
from app.models.Models import logged_in
class ActivitiesResource(Resource):

    @logged_in
    def get(self, bucket_id, user_id=None):
        if user_id is not None:
            bucketlist = Bucket.query.filter_by(user_id=user_id, bucket_id=bucket_id)
            if bucketlist:
                items = bucketlist.activities
                responseObject = []
                for item in items:
                    item = {
                        'id': item.id,
                        'name': item.name,
                        'created': item.created_at,
                        'modified': item.updated_at
                    }
                    responseObject.append(item)
                return make_response((responseObject))
            else:
                responseObject ={
                    'status': 'fail',
                    'message': 'bucketlist  does not exist'
                }
                return make_response((responseObject))





class ActivityResource(Resource):
    pass