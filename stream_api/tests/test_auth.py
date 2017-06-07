import unittest

import json
import time

from stream_api.tests.base import BaseTestCase

from common_functions import login_user, register_user
from config import AUTH_SERVER


class TestLoginServer(BaseTestCase):

    def test_register(self):
        """ Test that test user can create a user """
        register_response = register_user('yuanti','yuanti@gmail.com', 'freewifi')
        data = json.loads(register_response.text)
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['access_token'])
        self.assertTrue(data['refresh_token'])
        self.assertEqual(register_response.status_code, 201)

    def test_login(self):
        """User Login Test Function"""
        """ Test that test user can create a user """
        register_response = register_user('yuanti','yuanti@gmail.com', 'freewifi')
        data = json.loads(register_response.text)
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['access_token'])
        self.assertTrue(data['refresh_token'])
        self.assertEqual(register_response.status_code, 201)

        """ Test that test user can login """
        login_response = login_user('yuanti@gmail.com', 'freewifi')
        data = json.loads(login_response.text)
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['refresh_token'])
        self.assertTrue(data['access_token'])
        self.assertEqual(login_response.status_code, 200)
