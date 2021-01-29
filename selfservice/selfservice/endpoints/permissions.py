#!/usr/bin/env python3

# SchoolConnect SelfService API
# Permission API endpoint
# © 2020 - 2021 Johannes Kreutz.


# Include dependencies
from flask import Blueprint
from flask_login import login_required, current_user
import os


# Include modules
from modules.permissionCheck import permissionCheck
from modules.groupMembership import groupMembership


# Endpoint definition
permissionApi = Blueprint("permissionApi", __name__)


@permissionApi.route("/api/permissions/reset", methods=["GET"])
@login_required
def hasResetPermission():
    pCheck = permissionCheck()
    permissions = pCheck.get(current_user.username)
    if "emailrst" in permissions:
        return "GRANTED", 200
    else:
        return "NOT ALLOWED", 200


@permissionApi.route("/api/permissions/resetenabled", methods=["GET"])
def resetEnabled():
    isResetEnabled = os.environ.get("EMAIL_RESET_ENABLED")
    if isResetEnabled.lower() == "true":
        return "ENABLED", 200
    else:
        return "DISABLED", 200


@permissionApi.route("/api/permissions/isteacher", methods=["GET"])
@login_required
def isTeacher():
    gMember = groupMembership()
    if gMember.checkGroupMembership(current_user.username, "teachers"):
        return "GRANTED", 200
    else:
        return "NOT ALLOWED", 200


@permissionApi.route("/api/permissions/teacherreset/<id>", methods=["GET"])
@login_required
def canBeTeacherResetted(id):
    pCheck = permissionCheck()
    permissions = pCheck.get(current_user.username)
    if "pwalwrst" in permissions:
        return "GRANTED", 200
    else:
        return "NOT ALLOWED", 200


@permissionApi.route("/api/permissions/courselist", methods=["GET"])
@login_required
def hasCourselistPermission():
    pCheck = permissionCheck()
    permissions = pCheck.get(current_user.username)
    if "grouplst" in permissions:
        return "GRANTED", 200
    else:
        return "NOT GRANTED", 200
