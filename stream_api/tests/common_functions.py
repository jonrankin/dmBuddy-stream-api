# /api/tests/common_functions.py

import requests
import json

from config import AUTH_SERVER

def login_user(email, password):

    return requests.post(
        AUTH_SERVER + 'auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        headers = {
            'content-type' : 'application/json'
        }
    )


def register_user(username, email, password):
    return requests.post(
        AUTH_SERVER + 'auth/register',
        data=json.dumps(dict(
            email=email,
            password=password,
            username=username
        )),
        headers ={
            'content-type' : 'application/json'
        }
    )

def create_stream(self, token, stream_name, stream_desc=""):
    return self.client.post(
        '/stream',
        headers=dict(
            Authorization='Bearer ' + token
        ),
        data=json.dumps(dict(
            stream_name=stream_name,
            stream_desc=stream_desc
        )),
        content_type='application/json',
    )

