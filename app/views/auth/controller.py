from app.blueprints import auth_mod
from app.core.authentication import require_login, require_role, email_in_organization
from app.core.oauth_api import get_user_information
from app.models.users import User
from app.extensions import db

from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials

from flask import g, url_for, request, session, current_app, redirect, render_template, flash

from httplib2 import Http

import logging

import json

LOG = logging.getLogger(__name__)

@auth_mod.route('/')
def index():
    return 'auth blueprint test'

@auth_mod.route('/test')
def test():
    return render_template("base.html")

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

        user_information = get_user_information(credentials.to_json())

        if not email_in_organization(user_information['email'], 'stuy.edu'):
            LOG.debug('Non stuy.edu email')
            flash('You must user a stuy.edu email address')
            return redirect(url_for('public.controller.index'))

        session['credentials'] = credentials.to_json()

        user = User.query.filter_by(email = user_information['email']).first()

        LOG.info(user_information)

        if not user:
            u = User(email = user_information['email'])
            u.add_role('student')

            db.session.add(u)
            db.session.commit()

            session['id'] = u.id
        
        return redirect(url_for('public.controller.index'))


