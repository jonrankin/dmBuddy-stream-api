
import json

from flask import jsonify, make_response

def default_invalid_token_callback(error_string = 'Invalid Token'):
	"""
	Default method that is passed if a protected resource is accessed with an invalid token. Error string is returned to the function with a 401 status code

	:param error_string: A string that explains why this request is unauthorized
	"""

	return make_response(jsonify({'message':error_string, 'status':'fail'})), 401

def default_unauthorized_callback(error_string):
	"""
	Default method that is passed if a protected resource is accessed without a token. Error string is returned to the function with a 401 status code

	:param error_string: A string that explains why this request is unauthorized
	"""
        responseObject = {
              'status': 'fail',
              'message': error_string,
        }
        return jsonify(responseObject), 401


def default_needs_fresh_token_callback():
	"""
	Default method that is passed if an expired access token is used to access a protected resource,

	return a message that details Refresh is required with a 401 status code.
	"""
        responseObject = {
              'status': 'fail',
              'message': 'Refresh Required'
        }
	return make_response(jsonify(responseObject)), 401
