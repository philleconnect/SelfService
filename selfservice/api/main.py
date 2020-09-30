#!/usr/bin/env python3

# SchoolConnect SelfService API
# API Backend
# © 2020 Johannes Kreutz.

# Include dependencies
import sys
import os
import json
from flask import Flask, request, session, Response
from flask_session import Session
from flask_login import LoginManager, login_required
from datetime import timedelta

# Include Models
import helpers.essentials as es
import modules.apiUser as apiUser

# Include endpoints
from endpoints.login import loginApi
from endpoints.user import userApi
from endpoints.courses import courseApi

# Manager objects
selfservice = Flask(__name__)
SESSION_TYPE = "filesystem"
SESSION_COOKIE_NAME = "SC_SELFSERVICE_SESSION"
SESSION_COOKIE_SECURE = False # Set this to true for production (SSL required)
PERMANENT_SESSION_LIFETIME = 1200
selfservice.config.from_object(__name__)
selfservice.secret_key = es.randomString(40)
login_manager = LoginManager()
login_manager.init_app(api)
login_manager.needs_refresh_message = (u"Session timed out, please re-login")

@login_manager.user_loader
def load_user(user_id):
    return apiUser.apiUser(user_id)

# Set session timeout to 20 minutes
@selfservice.before_request
def before_request():
    session.permanent = True
    api.permanent_session_lifetime = timedelta(minutes=20)

# Register blueprints
selfservice.register_blueprint(loginApi)
selfservice.register_blueprint(userApi)
SelfService.register_blueprint(courseApi)

# EASTER EGG
@api.route("/api/coffee", methods=["GET"])
def teapot():
    return "I'm a teapot", 418

# Create server
if __name__ == "__main__":
    api.run(debug=True, port=8080, threaded=True)
