#!/usr/bin/env python3

# SchoolConnect SelfService API
# Login API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import passlib.hash
import os

# Include modules
import modules.database as db
import modules.apiUser as apiUser
import modules.permissionCheck as pc
import modules.groupMembership as gm

# Endpoint definition
loginApi = Blueprint("loginApi", __name__)
@loginApi.route("/api/login", methods=["POST"])
def createSession():
    dbconn = db.database()
    dbconn.execute("SELECT unix_hash, P.id FROM userpassword UP INNER JOIN people P ON UP.people_id = P.id WHERE P.username = %s", (request.form.get("uname"),))
    results = dbconn.fetchall()
    if not len(results) == 1:
        return "ERR_USERNAME_NOT_UNIQUE", 403
    if passlib.hash.ldap_salted_sha1.verify(request.form.get("passwd"), results[0]["unix_hash"]):
        user = apiUser.apiUser(results[0]["id"])
        login_user(user)
        pCheck = pc.permissionCheck()
        gMember = gm.groupMembership()
        return jsonify({"permissions":pCheck.get(current_user.username),"groups":gMember.getGroupsOfUser(current_user.username)}), 200
    else:
        return "ERR_ACCESS_DENIED", 401

@loginApi.route("/api/logout", methods=["POST"])
def removeSession():
    logout_user()
    return "SUCCESS", 200

@loginApi.route("/api/permissions/reset", methods=["GET"])
@login_required
def hasResetPermission():
    pCheck = pc.permissionCheck()
    permissions = pCheck.get(current_user.username)
    if "emailrst" in permissions:
        return "GRANTED", 200
    else:
        return "NOT ALLOWED", 200

@loginApi.route("/api/permissions/resetenabled", methods=["GET"])
def resetEnabled():
    isResetEnabled = os.environ.get("EMAIL_RESET_ENABLED")
    if isResetEnabled.lower() == "true":
        return "ENABLED", 200
    else:
        return "DISABLED", 200

@loginApi.route("/api/permissions/isteacher", methods=["GET"])
@login_required
def isTeacher():
    gMember = gm.groupMembership()
    if gMember.checkGroupMembership(current_user.username, "teachers"):
        return "GRANTED", 200
    else:
        return "NOT ALLOWED", 200

@loginApi.route("/api/permissions/teacherreset/<id>", methods=["GET"])
@login_required
def canBeTeacherResetted(id):
    pCheck = pc.permissionCheck()
    permissions = pCheck.get(current_user.username)
    if "pwalwrst" in permissions:
        return "GRANTED", 200
    else:
        return "NOT ALLOWED", 200

@loginApi.route("/api/permissions/courselist", methods=["GET"])
@login_required
def hasCourselistPermission():
    pCheck = pc.permissionCheck()
    permissions = pCheck.get(current_user.username)
    if "grouplst" in permissions:
        return "GRANTED", 200
    else:
        return "NOT GRANTED", 200
