import unittest
import json
from tests.Base import Base


class UserTestCase(Base):
    def test_user_registration(self):
        "Test a user can register."
        response = self.client().post('/authentication/register',
                                      data=self.user, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_password_mismatch(self):
        "Test user can not register with mismatching password."
        response = self.client().post('/authentication/register',
                                      data=self.user_password, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_taken_user_name(self):
        "Test user can not register with existing username."
        register = self.client().post('/authentication/register',
                                      data=self.user, content_type='application/json')
        response = self.client().post('/authentication/register',
                                      data=self.user, content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_register_short_password(self):
        "Test user can not register with short password."
        response = self.client().post('/authentication/register',
                                      data=self.short_pass, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_register_short_username(self):
        "Test user can not register with short username."
        response = self.client().post('/authentication/register',
                                      data=self.short_username, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        "Test registered user can login successfully."
        register = self.client().post('/authentication/register',
                                      data=self.user, content_type='application/json')
        response = self.client().post('/authentication/login', data=self.login,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_login_invalid_creadentials(self):
        "Test user cannot login with invalid credentials."
        register = self.client().post('/authentication/register',
                                      data=self.user, content_type='application/json')
        response = self.client().post('/authentication/login', data=self.invalid_login,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_unregistered_user(self):
        response = self.client().post('/authentication/login', data=self.login,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 401)
