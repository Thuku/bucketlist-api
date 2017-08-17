"""Authentication."""
from flask import Flask, request, make_response, json, jsonify
from flask_restful import reqparse, request, Resource
from app import db
from app.models.Models import User, Bucket, Activity
from app.models.Models import logged_in


class ActivitiesResource(Resource):

    @logged_in
    def get(self, bucketlist_id, user_id=None, res=None):
        if user_id is not None:
            bucketlist = Bucket.query.filter_by(
                user_id=user_id, id=bucketlist_id).first()
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
                responseObject = {
                    'status': 'fail',
                    'message': 'bucketlist  does not exist'
                }
                return make_response((responseObject))

    @logged_in
    def post(self, bucketlist_id, user_id=None, res=None):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()
        if len(args['name']) < 5:
            responseObject = {
                'status': 'fail',
                'message': "Activity should be more than 5 characters"
            }
            return make_response(jsonify(responseObject))

        else:
            if user_id is not None:
                bucketlist = Bucket.query.filter_by(
                    id=bucketlist_id, user_id=user_id).first()
                if bucketlist:
                    activity = Activity.query.filter_by(
                        bucket_id=bucketlist_id, name=args.get('name')).first()
                    if not activity:
                        activity = Activity(
                            name=args.get('name'),
                        )
                        bucketlist.activities.append(activity)
                        db.session.add(bucketlist)
                        db.session.commit()
                        responseObject = {
                            'status': 'successful',
                            'message': 'Activity successfuly created'
                        }
                        return make_response(jsonify(responseObject))
                    else:
                        responseObject = {
                            'status': 'fail',
                            'message': 'Activity Already exists'
                        }
                        return make_response(jsonify(responseObject))


class ActivityResource(Resource):
    pass
