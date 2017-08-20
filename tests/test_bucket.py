import unittest
import json
from tests.Base import Base


class BucketTestCase(Base):
    def test_create_bucket(self):
        "User can create bucketlist."
        register = self.client().post('/authentication/register',
                                      data=self.user, content_type='application/json')

        response = self.client().post('/bucket', data=self.bucket,
                                      headers=self.set_headers())

        self.assertEqual(response.status_code, 201)

    def test_create_existing_bucketlist(self):
        "User can not create bucketlist."
        result = self.create_user()
        first_bucket = self.client().post(
            '/bucket', data=self.bucket, headers=self.set_headers())
        second_bucket = self.client().post(
            '/bucket', data=self.bucket, headers=self.set_headers())
        self.assertEqual(second_bucket.status_code, 409)

    def test_get_buckets(self):
        "User can get buckets."
        self.create_user()
        # Without buckets
        response = self.client().get('/bucket', headers=self.set_headers())
        self.assertEqual(response.status_code, 200)
        bucket = self.client().post(
            '/bucket', data=self.bucket, headers=self.set_headers())

        response = self.client().get('/bucket', headers=self.set_headers())
        self.assertEqual(response.status_code, 200)
    def test_user_search_bucket(self):
        self.create_user()
        self.create_bucket()
        self.create_activity()
        response = response = self.client().get('/bucket?q=Mombasa adventures', headers=self.set_headers())
        self.assertEqual(response.status_code, 201)

    def test_bucket_short_name(self):
        self.create_user()
        response = self.client().post('/bucket', data=self.short_bucket,
                                      headers=self.set_headers())
        self.assertEqual(response.status_code, 401)

    def test_bucket_short_description(self):
        self.create_user()
        response = self.client().post('/bucket', data=self.short_description,
                                      headers=self.set_headers())
        self.assertEqual(response.status_code, 401)

    def test_user_get_bucket(self):
        self.create_user()
        # Get non existing bucket
        response = self.client().get('/bucket/1', headers=self.set_headers())
        self.assertEqual(response.status_code, 404)
        # Get existing bucket
        self.client().post('/bucket', data=self.bucket, headers=self.set_headers())
        response = self.client().get('/bucket/1', headers=self.set_headers())
        self.assertEqual(response.status_code, 200)

    def test_user_delete_bucket(self):
        self.create_user()
        # Delete a non exixting bucket.
        response = self.client().delete('/bucket/1', headers=self.set_headers())
        self.assertEqual(response.status_code, 404)

        # Delete existing bucketlist.
        self.client().post('/bucket', data=self.bucket, headers=self.set_headers())
        response = self.client().delete('/bucket/1', headers=self.set_headers())
        self.assertEqual(response.status_code, 200)

    def test_update_bucket(self):
        self.create_user()
        self.client().post('/bucket', data=self.bucket, headers=self.set_headers())
        response = self.client().put('/bucket/1', data=self.update_bucket,
                                     headers=self.set_headers())
        self.assertEqual(response.status_code, 200)
