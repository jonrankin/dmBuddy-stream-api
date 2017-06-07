# api/stream/views.py


from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from stream_api import bcrypt, db
from stream_api.db_access.models import User, Stream
from stream_api.auth_library import protected_resource

import json

stream_blueprint = Blueprint('stream', __name__)

from pprint import pprint

class StreamAPI(MethodView):
     """
     Stream Resource
     """

     @staticmethod
     def stream_get_authorized(claims, post_data):
         """ Method for displaying all streams for the user """
         return make_response(jsonify({
                 'status': 'success',
                 'data': {
                 }
               })), 200

     @staticmethod
     def stream_post_authorized(request, claims):
         """ Method for creating streams"""
         # get the post data
         post_data = request.get_json()


         # check if stream name already exists
         stream = Stream.query.filter_by(stream_name=post_data.get('stream_name'), created_by=claims['sub']).first()
         if not stream:
                    try:
                        stream = Stream(
                             stream_name=post_data.get('stream_name'),
                             stream_desc=post_data.get('stream_desc'),
                             created_by= claims['sub']
                        )
                        #insert the stream
                        db.session.add(stream)
                        db.session.commit()

                        #query for newly created stream
                        stream_data =  Stream.query.filter_by(stream_name=post_data.get('stream_name'), created_by=claims['sub']).first()
                        responseObject = {
                                'status': 'success',
                                 'stream':{
                                    'stream_id': stream_data.stream_id,
                                    'stream_name': stream_data.stream_name,
                                    'stream_desc': stream_data.stream_desc
                                 }
                        }
                        return make_response(jsonify(responseObject)), 201
                    except Exception as e:
                         responseObject = {
                             'status': 'fail',
                              'message': e
                         }
                         return make_response(jsonify(responseObject)), 401

     def get(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                stream = Stream.query.filter(user_id=resp)
                responseObject = {
                    'status': 'success',
                    'data': {
                    }
                }
                return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401

     def post(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        post_data = request.get_json()
        return make_response(protected_resource(request, self.stream_post_authorized, 'access'))

#define the API resources
stream_view = StreamAPI.as_view('stream_api')

#add rules for API endpoints
stream_blueprint.add_url_rule(
    '/stream',
    view_func=stream_view,
    methods=['GET', 'POST']
)
