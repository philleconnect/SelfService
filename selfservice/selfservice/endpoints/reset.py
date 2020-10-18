#!/usr/bin/env python3

# SchoolConnect SelfService API
# Password email reset API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import requests
import passlib.hash

# Include modules
import modules.database as db
import helpers.hash as hash
import helpers.resetEmail as email

# Endpoint definition
resetApi = Blueprint("resetApi", __name__)
@resetApi.route("/api/reset/start", methods=["PUT"])
def createResetSession():
    return None
