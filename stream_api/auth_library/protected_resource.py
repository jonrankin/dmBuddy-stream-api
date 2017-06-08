# auth_library/protected_resource.py

from stream_api.db_access.models import User
from .default_callbacks import default_unauthorized_callback,  default_needs_fresh_token_callback

import requests

def protected_resource(request, authorized_callback, token_needed = 'access', unauthorized_callback = default_unauthorized_callback, *args, **kwargs):
        """
        Method used to protect a resource. This is used in a view to determine whether they are authorized or unauthorized. User passes an$

        :param auth_token: Token the user is attempting to authorized with.
        :param authorized_callback: This is a callback method we used to return a json string to the view to be presented. The callback me$
        :param unauthorized_callback: If there is still information that we want to present if the token is not authorized we can pass a c$
        """
        auth_token = request.headers.get('Authorization')

        # If a valid auth_token is present
        if auth_token:
                auth_token = auth_token.split(" ")[1]
                resp = User.decode_token(auth_token, token_needed)
                #when decoding the token, if the response is not a string, else we have an error and pass it to the default_expired_token_$
                if not isinstance(resp, str):
                        return authorized_callback(resp, request, *args, **kwargs)
                elif resp == 'Expired':
                        return default_needs_fresh_token_callback
                return unauthorized_callback('Unauthorized')
        else:
                return unauthorized_callback('Unauthorized')

