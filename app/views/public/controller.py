from app.blueprints import public_mod
from flask import g, url_for, request, session, current_app, redirect

@public_mod.route('/')
def index():
    return 'public blueprint test'
