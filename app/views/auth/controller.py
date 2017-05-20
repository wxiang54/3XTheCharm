from app.blueprints import auth_mod
from app.core.authentication import require_login, require_role

from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials

from flask import g, url_for, request, session, current_app, redirect

from httplib2 import Http

import logging

import json

LOG = logging.getLogger(__name__)

@auth_mod.route('/')
def index():
    return 'auth blueprint test'

@auth_mod.route('/login')
def login():
    flow = flow_from_clientsecrets('app/static/' + current_app.config['OAUTH_CLIENT_SECRETS'],
                                   scope = 'https://www.googleapis.com/auth/userinfo.email',
                                   redirect_uri = url_for('auth.controller.login', _external = True))

    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        
        return redirect(url_for('auth.controller.login'))
