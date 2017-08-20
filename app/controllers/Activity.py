"""Authentication."""
from flask import Flask, request, make_response, json, jsonify
from flask_restful import reqparse, request, Resource
from werkzeug.exceptions import NotFound
from app import db
from app.models.Models import User, Bucket, Activity
from app.controllers.login import logged_in

class ActivitiesResource(Resource):

    @logged_in
    def get(self, bucketlist_id, user_id=None, res=None):
        if user_id is not None:
            bucketlist = Bucket.query.filter_by(
                user_id=user_id, id=bucketlist_id).first()
            if bucketlist:
                items = bucketlist.activities
                if len(items) == 0:
                    responseObject = {
                        'status': 'alert',
                        'message': 'Add activities to your bucketlist'
                    }
                    return make_response((responseObject), 200)
                responseObject = []
                for item in items:
                    item = {
                        'id': item.id,
                        'name': item.name,
                        'bucket_id': item.bucket_id,
                        'created': item.created_at,
                        'modified': item.updated_at
                    }
                    responseObject.append(item)
                return make_response((responseObject), 201)
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'bucketlist  does not exist'
                }
                return make_response((responseObject), 404)

    @logged_in
    def post(self, bucketlist_id, user_id=None, res=None):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location='json')
        args = parser.parse_args()
        if len(args['name']) < 5:
            responseObject = {
                'status': 'fail',
                'message': "Activity should be more than 5 characters"
            }
            return make_response(jsonify(responseObject), 401)

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
                        return make_response(jsonify(responseObject), 200)
                    else:
                        responseObject = {
                            'status': 'fail',
                            'message': 'Activity Already exists'
                        }
                        return make_response(jsonify(responseObject), 409)


class ActivityResource(Resource):

    @logged_in
    def delete(self, bucketlist_id, item_id, user_id=None, res=None):
        if user_id is not None:
            bucket = Bucket.query.filter_by(id=bucketlist_id).first()
            if bucket and bucket.user_id == user_id:
                activity = Activity.query.filter_by(
                    bucket_id=bucketlist_id, id=item_id).first()
                db.session.delete(activity)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Activity successfully deleted'
                }
                return make_response(jsonify(responseObject), 200)
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'You have no such Activity in your bucketlist'
                }
                return make_response(jsonify(responseObject), 404)
        else:
            responseObject = res
            return make_response(jsonify(responseObject))

    @logged_in
    def get(self, bucketlist_id, item_id, user_id=None, res=None):
        if user_id is not None:
            bucket = Bucket.query.filter_by(id=bucketlist_id).first()
            if bucket and bucket.user_id == user_id:
                activity = Activity.query.filter_by(
                    id=item_id, bucket_id=bucketlist_id).first()
                if activity is None:
                    raise NotFound("wewe wacha")
                responseObject = {
                    'name': activity.name
                }
                return make_response(jsonify(responseObject))

    @logged_in
    def put(self, bucketlist_id, item_id, user_id=None, res=None):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        args = parser.parse_args()
        bucket = Bucket.query.filter_by(
            user_id=user_id, id=bucketlist_id).first()
        if bucket and user_id is not None:
            if user_id == bucket.user_id:
                activity = Activity.query.filter_by(
                    id=item_id, bucket_id=bucketlist_id).first()
                if activity is None:
                    raise NotFound("wewe wacha")
                if activity:
                    activity.name = args['name']
                    db.session.add(activity)
                    db.session.commit()
                    responseObject = {
                        'status': 'success',
                        'message': 'Activity successfully Updated'
                    }
                return make_response(jsonify(responseObject))
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Error updating bucketlist activity'
                }
                return make_response(jsonify(responseObject))
