# api/tests/test_stream.py

import unittest

from stream_api import db
from stream_api.db_access.models import User, Stream
from stream_api.tests.base import BaseTestCase

import json
import time

from common_functions import register_user, login_user, create_stream

class TestStreamBlueprint(BaseTestCase):

  def test_stream_create(self):
        # user registration
        resp_register = register_user('yuanti', 'yuanti@gmail.com', 'freewifi')
        data_register = json.loads(resp_register.text)
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(data_register['access_token'])
        self.assertEqual(resp_register.status_code, 201)

        # user login
        resp_login = login_user('yuanti@gmail.com', 'freewifi')
        data_login = json.loads(resp_login.text)
        self.assertTrue(data_login['status'] == 'success')
        self.assertTrue(data_login['message'] == 'Successfully logged in.')
        self.assertTrue(data_login['access_token'])
        self.assertEqual(resp_login.status_code, 200)

        #create stream
        resp_stream = create_stream(self, data_login['access_token'], 'World of Adventures', 'silly_stuff')
        data_stream = json.loads(resp_stream.data.decode())
        self.assertTrue(data_login['status'] == 'success')


  def test_create_stream(self):
       """ Test that we can create a stream for a user """

       with self.client:
        # user registration
        resp_register = register_user('yuanti', 'yuanti@gmail.com', 'freewifi')
        data_register = json.loads(resp_register.text)
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(data_register['access_token'])
        self.assertEqual(resp_register.status_code, 201)

        # user login
        resp_login = login_user('yuanti@gmail.com', 'freewifi')
        data_login = json.loads(resp_login.text)
        self.assertTrue(data_login['status'] == 'success')
        self.assertTrue(data_login['message'] == 'Successfully logged in.')
        self.assertTrue(data_login['access_token'])
        self.assertEqual(resp_login.status_code, 200)

        #create stream
        resp_stream = create_stream(self, data_login['access_token'], 'World of Adventures', 'silly_stuff')
        data_stream = json.loads(resp_stream.data.decode())
        self.assertTrue(data_login['status'] == 'success')

  def test_create_stream_with_existing(self):
       """ Test that we can pull all streams associated to user """

       with self.client:
        # user registration
        resp_register = register_user('yuanti', 'yuanti@gmail.com', 'freewifi')
        data_register = json.loads(resp_register.text)
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(data_register['access_token'])
        self.assertEqual(resp_register.status_code, 201)

        # user login
        resp_login = login_user('yuanti@gmail.com', 'freewifi')
        data_login = json.loads(resp_login.text)
        self.assertTrue(data_login['status'] == 'success')
        self.assertTrue(data_login['message'] == 'Successfully logged in.')
        self.assertTrue(data_login['access_token'])
        self.assertEqual(resp_login.status_code, 200)

        #create stream
        resp_stream = create_stream(self, data_login['access_token'], 'World of Adventures', 'silly_stuff')
        data_stream = json.loads(resp_stream.data.decode())
        self.assertTrue(data_stream['status'] == 'success')

        #create stream
        resp_stream = create_stream(self, data_login['access_token'], 'World of Adventures', 'silly_stuff')
        data_stream = json.loads(resp_stream.data.decode())
        self.assertTrue(data_stream['status'] == 'fail')


  def test_list_stream(self):
       """ Test that we can pull all streams associated to user """

       with self.client:
        # user registration
        resp_register = register_user('yuanti', 'yuanti@gmail.com', 'freewifi')
        data_register = json.loads(resp_register.text)
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(data_register['access_token'])
        self.assertEqual(resp_register.status_code, 201)

        # user login
        resp_login = login_user('yuanti@gmail.com', 'freewifi')
        data_login = json.loads(resp_login.text)
        self.assertTrue(data_login['status'] == 'success')
        self.assertTrue(data_login['message'] == 'Successfully logged in.')
        self.assertTrue(data_login['access_token'])
        self.assertEqual(resp_login.status_code, 200)

        #create stream
        resp_stream = create_stream(self, data_login['access_token'], 'World of Adventures', 'silly_stuff')
        data_stream = json.loads(resp_stream.data.decode())
        self.assertTrue(data_login['status'] == 'success')

        #create stream
        resp_stream = create_stream(self, data_login['access_token'], 'World of Adventures Redux', 'silly_stuff')
        data_stream = json.loads(resp_stream.data.decode())
        self.assertTrue(data_login['status'] == 'success')

        #list stream
        resp_list = self.client.get(
                      '/stream',
                      headers=dict(
                          Authorization='Bearer ' + data_login['access_token']
                      ),
                      content_type='application/json'
        )
        data_list = json.loads(resp_list.data.decode())
        self.assertTrue(data_list['status'] == 'success')
        self.assertTrue(data_list['data']['1']['stream_name'] == 'World of Adventures')
        self.assertTrue(data_list['data']['2']['stream_name'] == 'World of Adventures Redux')

  def test_stream_details(self):
       """ Test that we can pull a specific streams details """

       with self.client:
        # user registration
        resp_register = register_user('yuanti', 'yuanti@gmail.com', 'freewifi')
        data_register = json.loads(resp_register.text)
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(data_register['access_token'])
        self.assertEqual(resp_register.status_code, 201)

        # user login
        resp_login = login_user('yuanti@gmail.com', 'freewifi')
        data_login = json.loads(resp_login.text)
        self.assertTrue(data_login['status'] == 'success')
        self.assertTrue(data_login['message'] == 'Successfully logged in.')
        self.assertTrue(data_login['access_token'])
        self.assertEqual(resp_login.status_code, 200)

        #create stream
        resp_stream = create_stream(self, data_login['access_token'], 'World of Adventures', 'silly_stuff')
        data_stream = json.loads(resp_stream.data.decode())
        self.assertTrue(data_login['status'] == 'success')

        resp_details = self.client.get(
                      '/stream/1',
                      headers=dict(
                          Authorization='Bearer ' + data_login['access_token']
                      ),
                      content_type='application/json'
        )
        data_list = json.loads(resp_details.data.decode())
        self.assertTrue(data_list['status'] == 'success')
        self.assertTrue(data_list['data']['stream_name'] == 'World of Adventures')


if __name__ == '__main__':
      unittest.main()
