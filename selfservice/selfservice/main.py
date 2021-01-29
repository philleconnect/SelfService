#!/usr/bin/env python3

# SchoolConnect SelfService API
# API Backend
# © 2020 - 2021 Johannes Kreutz.


# Include dependencies
import sys
import os
import json
from flask import Flask, request, session, Response
from flask_session import Session
from flask_login import LoginManager, login_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta


# Include Models
import config
import helpers.essentials as es
from modules.apiUser import apiUser


# Run first setup
if not os.path.exists(config.CONFIG_SECRET_KEY):
    with open(config.CONFIG_SECRET_KEY, "w") as f:
        f.write(es.randomString(40))


# Include endpoints
from endpoints.login import loginApi
from endpoints.user import userApi
from endpoints.courses import courseApi
from endpoints.reset import resetApi
from endpoints.permissions import permissionApi


# Manager objects
selfservice = Flask(__name__)
SESSION_TYPE = "filesystem"
SESSION_COOKIE_NAME = "SC_SELFSERVICE_SESSION"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
PERMANENT_SESSION_LIFETIME = 1200
selfservice.config.from_object(__name__)
with open(config.CONFIG_SECRET_KEY, "r") as f:
    selfservice.secret_key = f.read()
login_manager = LoginManager()
login_manager.init_app(selfservice)
login_manager.needs_refresh_message = (u"Session timed out, please re-login")
limiter = Limiter(
    selfservice,
    key_func=get_remote_address,
    default_limits=["500 per day", "100 per hour"]
)
limiter.limit("1/second")(loginApi)


@login_manager.user_loader
def load_user(user_id):
    return apiUser(user_id)


# Set session timeout to 20 minutes
@selfservice.before_request
def before_request():
    session.permanent = True
    selfservice.permanent_session_lifetime = timedelta(minutes=20)


# Register blueprints
selfservice.register_blueprint(loginApi)
selfservice.register_blueprint(userApi)
selfservice.register_blueprint(courseApi)
selfservice.register_blueprint(resetApi)
selfservice.register_blueprint(permissionApi)


# EASTER EGG
@selfservice.route("/api/coffee", methods=["GET"])
@limiter.exempt  # Give the people as many tea as they want!
def teapot():
    return "I'm a teapot", 418


# Create server (only executed in debug mode, production via uwsgi)
if __name__ == "__main__":
    selfservice.run(debug=True, port=8080, threaded=True)
