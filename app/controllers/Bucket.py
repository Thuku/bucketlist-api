"""Authentication."""
from flask import Flask, request, make_response, json, jsonify
from flask_restful import reqparse, request, Resource
from werkzeug.exceptions import NotFound
from app import db
from app.models.Models import User, Bucket
from app.models.Models import logged_in


class BucketsResource(Resource):

    @logged_in
    def get(self, user_id=None, res=None):
        page = request.args.get('page', type=int, default=1)
        limit = request.args.get('limit', type=int, default=5)
        if user_id is not None:
            bucketlists = Bucket.query.filter_by(
                user_id=user_id).paginate(page, limit, False).items
            if len(bucketlists) == 0:
                responseObject = {
                    'status': 'alert',
                    'message': 'Create bucketlist'
                }
                return make_response((responseObject))
            else:
                responseObject = []
                for bucketlist in bucketlists:
                    bucket = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'description': bucketlist.description,
                        'created': bucketlist.created_at,
                        'modified': bucketlist.updated_at
                    }
                    responseObject.append(bucket)
                return make_response((responseObject))

    @logged_in
    def post(self, user_id=None, res=None):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, location="json")
        parser.add_argument('description', type=str,
                            required=True, location="json")
        args = parser.parse_args()
        if len(args['name']) < 5:
            responseObject = {
                'status': 'Fail',
                'message': 'Bucketlist name should be at least 5 characters'
            }
            return make_response(jsonify(responseObject), 401)
        elif len(args['description']) < 5:
            responseObject = {
                'status': 'Fail',
                'message': 'Bucketlist Description should be at least 5 characters'
            }
            return make_response(jsonify(responseObject), 401)
        else:
            if user_id is not None:
                bucketlist = Bucket.query.filter_by(
                    name=args.get('name')).first()

                if not bucketlist:
                    bucketlist = Bucket(
                        name=args.get('name'),
                        description=args.get('description'),
                        user_id=user_id
                    )
                    db.session.add(bucketlist)
                    db.session.commit()
                    responseObject = {
                        'status': 'successful',
                        'message': 'Bucketlist created successfully'
                    }
                    return make_response(jsonify(responseObject), 201)
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Bucketlist already exists'
                    }
                    return make_response(jsonify(responseObject), 409)


class BucketResource(Resource):

    @logged_in
    def get(self, bucket_id, user_id=None, res=None):
        if user_id is not None:
            bucket = Bucket.query.filter_by(
                user_id=user_id, id=bucket_id).first()
            if bucket is None:
                raise NotFound("wewe wacha")
            responseObject = {
                'name': bucket.name,
                'description': bucket.description,
                'created': bucket.created_at,
                'updated': bucket.updated_at
            }

            return make_response(jsonify(responseObject))

    @logged_in
    def delete(self, bucket_id, user_id=None, res=None):
        if user_id is not None:
            bucket = Bucket.query.filter_by(id=bucket_id).first()
            if bucket and bucket.user_id == user_id:
                db.session.delete(bucket)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Bucketlist successfully deleted'
                }
                return make_response(jsonify(responseObject))
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'You have no such bucketlist'
                }
                return make_response(jsonify(responseObject), 404)

    @logged_in
    def put(self, bucket_id, user_id=None, res=None):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        parser.add_argument('description', type=str, location='json')
        args = parser.parse_args()
        bucket = Bucket.query.filter_by(user_id=user_id, id=bucket_id).first()
        print(user_id, bucket_id)

        if bucket and user_id is not None:
            bucket.name = args['name']
            db.session.add(bucket)
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message': 'Bucketlist successfully Updated'
            }
            return make_response(jsonify(responseObject))
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Error updating bucketlist'
            }
            return make_response(jsonify(responseObject))
