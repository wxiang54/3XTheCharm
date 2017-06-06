from app.blueprints import public_mod
from flask import g, url_for, request, session, current_app, redirect

@public_mod.route('/')
def index():
    return redirect(url_for("auth.controller.login"))
