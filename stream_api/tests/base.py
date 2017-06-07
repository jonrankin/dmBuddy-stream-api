# api/tests/base.py


from flask_testing import TestCase

from stream_api import app, db

from common_functions import register_user, login_user

class BaseTestCase(TestCase):
    """ Base Tests """


    def create_app(self):
        app.config.from_object('stream_api.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def create_test_user(self):
        register_response = register_user('yuanti','yuanti@gmail.com', 'freewifi')
        data = json.loads(register_response.text)
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['access_token'])
        self.assertTrue(data['refresh_token'])
        self.assertEqual(register_response.status_code, 201)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
