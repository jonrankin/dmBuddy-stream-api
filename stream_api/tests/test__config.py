# api/tests/test_config.py

import unittest

from flask import current_app
from flask_testing import TestCase

from stream_api import config, app


class TestConfig(TestCase):
   def create_app(self):
       app.config.from_object('stream_api.config.AppConfig')
       return app

   def test_app_config_production(self):
        self.assertTrue(app.config['DEBUG'] is False)

class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('stream_api.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['DEBUG'])




if __name__ == '__main__':
     unittest.main()
