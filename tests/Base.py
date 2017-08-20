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
        self.headers = {

        }
        # Registration
        self.user = json.dumps({
            "username": "superman",
            "password": "password",
            "confirm_password": "password",
            "email": "superman@test.com"
        })

        # Registration with password mismatch
        self.user_password = json.dumps({
            "username": "superman",
            "password": "password",
            "confirm_password": "pasdsad",
            "email": "superman@test.com"
        })

        # Login
        self.login = json.dumps({
            "username": "superman",
            "password": "password"
        })

        # Login invalid credentials
        self.invalid_login = json.dumps({
            "username": "superman",
            "password": "pasasas"
        })

        # Short password
        self.short_pass = json.dumps({
            "username": "superman",
            "password": "pa",
            "confirm_password": "pa",
            "email": "superman@test.com"
        })
        # Registration with short username
        self.short_username = json.dumps({
            "username": "sup",
            "password": "password",
            "confirm_password": "password",
            "email": "superman@test.com"
        })
        # Create bucket.
        self.bucket = json.dumps({
            "name": "Mombasa adventures",
            "description": "Visit the coastal town of mombasa and engage in thrilling activities"
        })
        # Bucketlist with short name
        self.short_bucket = json.dumps({
            "name": "test",
            "description": "humanity can not govern" 
        })
        self.short_description = json.dumps({
            "name": "test humanity",
            "description": "hum" 
        })

        self.update_bucket = json.dumps({
            "name": "police june",
            "description" : "black lives matter"
        })

        self.activity = json.dumps({
            "name": "Hit the liqour store"
        })

        self.short_activity = json.dumps({
            "name": "Hit"
        })

        self.update_activity = json.dumps({
            "name": "Humanity at its best"
        })

    def set_headers(self):
        # login to server and get token
        payload = self.client().post('/authentication/login', data=self.login,
                                     content_type='application/json')

        response = json.loads(payload.data.decode())
        return {
            # HEADERS
            "Authorization": response["token"],
            "Content-Type": "application/json"

        }

    def create_user(self):
        user = self.client().post('/authentication/register',
                                  data=self.user, content_type='application/json')
        return user
    def create_bucket(self):
        bucket = self.client().post('/bucket', data=self.bucket,
                                      headers=self.set_headers())
    
    def create_activity(self):
        activity = self.client().post('/bucket/1/items', data=self.activity, headers=self.set_headers())

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
