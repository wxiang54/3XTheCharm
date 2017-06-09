from app.blueprints import public_mod
from flask import g, url_for, request, session, current_app, redirect, render_template

@public_mod.route('/')
def index():
    return render_template("welcome.html")
