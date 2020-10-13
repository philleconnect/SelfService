#!/usr/bin/env python3

# SchoolConnect SelfService API
# User API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user

# Include modules
import modules.database as db

# Endpoint definition
userApi = Blueprint("userApi", __name__)
@userApi.route("/api/user/data", methods=["GET", "PUT"])
@login_required
def myData():
    return None
