""" Collection of methods for getting information from Google """

from flask import session

from oauth2client.client import OAuth2Credentials

import json

from httplib2 import Http

def get_user_information(credentials):
    """ Given credentials, it will return the json information object of the person logged in

    :param credentials: The jsonnable string usually stored in session
    :type credentials: str
    """
    credentials = OAuth2Credentials.from_json(credentials)
    
    http_auth = credentials.authorize(Http())
    
    response, content = http_auth.request('https://www.googleapis.com/oauth2/v1/userinfo?alt=json')
    
    c = json.loads(content)
    
    return c

