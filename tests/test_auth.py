import unittest
import json

from app import create_app, db

app = create_app("testing")


class Base(unittest.TestCase):


    def setUp(self):

        self.client = app.test_client
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_registration(self):
        "Test a user can register."
        response = self.client().post('/authentication/register', data=json.dumps({
            "username": "superman",
            "password": "password",
            "confirm_password": "password",
            "email": "superman@test.com"}
        ),
        content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
    def test_user_login(self):
        response_register = self.test_user_registration()
        response = self.client().post('/authentication/login', data=json.dumps({
            "username": "superman",
            "password": "password"
        }
        ),
        content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
    def test_incorrect_user_registration(self):
        response = self.client().post('/authentication/register', data=dict(
            username="superman",
            password="password",
            confirm_password="passwo",
            email="superman@test.com"
        ), content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        response = self.client().post('/authentication/register', data=json.dumps({
            "username": "superman",
            "password": "password",
            "email": "superman@test.com"
        }
        ))
        self.assertEqual(response.status_code, 400)
        response = self.client().post('/authentication/register', data=json.dumps({
            "username": "sup",
            "password": "password",
            "confirm_password": "password",
            "email": "superman@test.com"}
        ),
        content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client().post('/authentication/register', data=dict(
            username="superman",
            password="password",
            confirm_password="password"        ))
        self.assertEqual(response.status_code, 400)



if __name__ == "__main__":
    unittest.main()