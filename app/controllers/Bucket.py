"""Authentication."""
from flask import Flask, request, make_response, json, jsonify
from flask_restful import reqparse, request, Resource
from app import  db
from app.models.Models import User, Bucket
from app.models.Models import logged_in
class BucketsResource(Resource):

    @logged_in
    def get(self, user_id = None, res = None):
        if user_id is not None:
            bucketlists = Bucket.query.filter_by(user_id=user_id).all()
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
    def post(self, user_id=None, res = None):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        args = parser.parse_args()
        if len(args['name']) < 5:
            responseObject = {
                'status': 'Fail',
                'message': 'Bucketlist name should be at least 5 characters'
            }
            return make_response(jsonify(responseObject))
        elif len(args['description']) < 5:
            responseObject = {
                'status': 'Fail',
                'message': 'Bucketlist Description should be at least 5 characters'
            }
            return make_response(jsonify(responseObject))
        else:
            if user_id is not None:
                bucketlist = Bucket.query.filter_by(name=args.get('name')).first()

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
                    return make_response(jsonify(responseObject))
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Bucketlist already exists'
                    }
                    return make_response(jsonify(responseObject))


class BucketResource(Resource):

    @logged_in
    def get(self, bucket_id, user_id=None, res=None):
        if user_id is not None:
            bucket = Bucket.query.filter_by(id=bucket_id).first()
            responseObject = {
                'name': bucket.name,
                'description': bucket.description,
                'created': bucket.created_at,
                'updated': bucket.updated_at
            }
            return make_response(jsonify(responseObject))




    @logged_in
    def put(self):
        pass

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
                return make_response(jsonify(responseObject))
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Bucket does not exist'
            }
            return make_response(jsonify(responseObject))

    @logged_in
    def patch(self):
        pass

    @logged_in
    def put(self, bucket_id, user_id=None, res=None):

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
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



            # if len(args['name'].strip()) < 5 or len(args['description'].strip()) < 5:
            #     responseObject = {
            #         'status': 'fail',
            #         'message': 'Name/Description should be Five characters or more'
            #     }
            #     return make_response(jsonify(responseObject))
            # else:
            #     bucket.name = args['name']
            #     bucket.description = args['description']






