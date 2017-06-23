from stuybulletin.blueprints import public_mod
from flask import g, url_for, request, session, current_app, redirect, render_template, flash

@public_mod.route('/')
def index():
    if "id" in session and "token" in session and g.user:
        flash("Welcome back!")
        if g.user.check_role("admin"):
            return redirect(url_for("admin.controller.opportunities"))
        else: #assume it's a student
            return redirect(url_for("student.controller.opportunities"))
    return render_template("welcome.html")
