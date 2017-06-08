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
     def stream_get_authorized(claims, *args, **kwargs):
         """ Method for displaying all streams for the user """

         stream_data =  Stream.query.filter_by(created_by=claims['sub'])
         user_streams = {}
         for _ in stream_data:
             user_streams[_.stream_id] ={
                               'stream_name': _.stream_name,
                               'stream_desc' : _.stream_desc
                             }
         responseObject = {
                              'status': 'success',
                              'data': user_streams
                          }

         return make_response(jsonify(responseObject)), 200

     @staticmethod
     def stream_post_authorized(claims, *args, **kwargs):
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
         else:
                  return make_response(jsonify({
                         'status': 'fail',
                         'message' : 'stream name already exists'
                  })), 202

     def get(self):
        return make_response(protected_resource(request, self.stream_get_authorized, 'access'))

     def post(self):
        return make_response(protected_resource(request, self.stream_post_authorized, 'access'))

class StreamDetailsAPI(MethodView):
     """
     stream details resource
     """

     @staticmethod
     def stream_details_authorized(claims, *args, **kwargs):
         stream_details = Stream.query.filter_by(stream_id=kwargs['user_id']).first()
         if stream_details: 
              return make_response(jsonify({
                      'status': 'success',
                      'data' : {
                             'stream_id' : kwargs['user_id'],
                             'stream_name' : stream_details.stream_name,
                             'stream_desc' : stream_details.stream_desc
                      }
              })), 200
         else:
              return make_response(jsonify({
                      'status': 'fail',
                      'message' : 'stream does not exist'
              })), 200

     def get(self, user_id):
        return make_response(protected_resource(request, self.stream_details_authorized, 'access', user_id= user_id))


#define the API resources
stream_view = StreamAPI.as_view('stream_api')
stream_detail_view = StreamDetailsAPI.as_view('stream_details_api')

#add rules for API endpoints
stream_blueprint.add_url_rule(
    '/stream',
    view_func=stream_view,
    methods=['GET', 'POST']
)
stream_blueprint.add_url_rule(
    '/stream/<int:user_id>',
    view_func=stream_detail_view,
    methods=['GET']
)
