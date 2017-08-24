import unittest
import json
from tests.Base import Base


class BucketTestCase(Base):

    def test_create_activity(self):
        self.create_user()
        self.client().post('/bucket', data=self.bucket,
                           headers=self.set_headers())
        response = self.client().post('/bucket/1/items', data=self.activity,
                                      headers=self.set_headers())
        self.assertEqual(response.status_code, 200)

    def test_create_short_activity(self):
        self.create_user()
        self.client().post('/bucket', data=self.bucket,
                           headers=self.set_headers())
        response = self.client().post('/bucket/1/items', data=self.short_activity,
                                      headers=self.set_headers())
        self.assertEqual(response.status_code, 401)

    def test_dupicate_activity(self):
        self.create_user()
        self.client().post('/bucket', data=self.bucket,
                           headers=self.set_headers())
        self.client().post('/bucket/1/items', data=self.activity,
                           headers=self.set_headers())
        response = self.client().post('/bucket/1/items', data=self.activity,
                                      headers=self.set_headers())
        self.assertEqual(response.status_code, 409)

    def test_get_activities(self):

        # Non existent bucket
        self.create_user()
        response = self.client().get('/bucket/1/items',
                                     headers=self.set_headers())
        self.assertEqual(response.status_code, 404)

        # Empty bucket
        self.create_bucket()
        response = self.client().get('/bucket/1/items',
                                     headers=self.set_headers())
        self.assertEqual(response.status_code, 200)

        # Bucket with an activity

        self.create_activity()
        response = self.client().get('/bucket/1/items',
                                     headers=self.set_headers())

        self.assertEqual(response.status_code, 201)

    def test_delete_activity(self):
        self.create_user()
        self.client().post('/bucket', data=self.bucket,
                           headers=self.set_headers())
        self.client().post('/bucket/1/items', data=self.activity,
                           headers=self.set_headers())
        response = self.client().delete('/bucket/1/item/1', data=self.activity,
                                        headers=self.set_headers())
        self.assertEqual(response.status_code, 200)

    def test_delete_non_existing_activity(self):
        self.create_user()
        response = self.client().delete('/bucket/1/item/1', data=self.activity,
                                        headers=self.set_headers())
        self.assertEqual(response.status_code, 404)

    def test_get_specific_activity(self):
        self.create_user()
        self.create_bucket()
        # Non existing activity
        response = self.client().get('/bucket/1/item/1', headers=self.set_headers())
        self.assertEqual(response.status_code, 404)
        # Existing activity
        self.create_activity()
        response = self.client().get('/bucket/1/item/1', headers=self.set_headers())
        self.assertEqual(response.status_code, 200)

    def test_update_activity(self):
        self.create_user()
        self.client().post('/bucket', data=self.bucket,
                           headers=self.set_headers())
        self.client().post('/bucket/1/items', data=self.activity,
                           headers=self.set_headers())
        response = self.client().put('/bucket/1/item/1', data=self.update_activity,
                                     headers=self.set_headers())
