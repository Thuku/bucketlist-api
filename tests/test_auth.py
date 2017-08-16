import unittest

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

    def test_login(self):
        response = self.client().post('/authentication/register', data=dict(
            username="superman",
            password="password",
            confirm_password="password",
            email="superman@test.com"
        ))
        self.assertEqual(response.status_code, 201)

if __name__ == "__main__":
    unittest.main()