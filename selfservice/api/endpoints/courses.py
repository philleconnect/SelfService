#!/usr/bin/env python3

# SchoolConnect SelfService API
# Course API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user

# Include modules
import modules.database as db

# Endpoint definition
courseApi = Blueprint("courseApi", __name__)
@courseApi.route("/api/course/my", methods=["GET"])
@login_required
def getMyCourses():
    return None
