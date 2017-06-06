from app.blueprints import auth_mod
from app.core.authentication import require_login, require_role, email_in_organization
from app.core.oauth_api import get_user_information
from app.models.users import User
from app.extensions import db
from oauth2client.client import flow_from_clientsecrets, OAuth2Credentials, AccessTokenCredentials
from flask import g, url_for, request, session, current_app, redirect, render_template, flash
from httplib2 import Http
import logging
import json
import requests

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

        user_information = get_user_information(credentials.to_json())

        if not email_in_organization(user_information['email'], 'stuy.edu'):
            LOG.debug('Non stuy.edu email')
            flash('You must use a stuy.edu email address')
            return redirect(url_for('public.controller.index'))

        session['token'] = credentials.access_token

        u = User.query.filter_by(email = user_information['email']).first()

        LOG.info(user_information)

        if not u:
            u = User(email = user_information['email'])
            u.add_role('student')

            db.session.add(u)
            db.session.commit()

        session['id'] = u.id
        return redirect(url_for('public.controller.index'))


@auth_mod.route('/logout')
def logout():
    r = requests.get('https://accounts.google.com/o/oauth2/revoke', params={"token": session["token"]})
    session.pop("token", None)
    session.pop("id", None)
    flash("Successfully logged out!", "success")
    return redirect(url_for('public.controller.index'))

#<class 'oauth2client.client.OAuth2Credentials'>
