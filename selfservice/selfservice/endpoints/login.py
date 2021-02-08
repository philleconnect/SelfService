#!/usr/bin/env python3

# SchoolConnect SelfService API
# Login API endpoint
# © 2020 - 2021 Johannes Kreutz.


# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
import passlib.hash


# Include modules
from modules.database import database
from modules.apiUser import apiUser
from modules.permissionCheck import permissionCheck
from modules.groupMembership import groupMembership
from modules.bruteforceProtection import bruteforceProtection


# Endpoint definition
loginApi = Blueprint("loginApi", __name__)


@loginApi.route("/api/login", methods=["POST"])
def createSession():
    bf = bruteforceProtection()
    timeout = bf.isBlocked(request.form.get("uname"))
    if timeout > 0:
        return jsonify({
            "status": "ERR_TOO_MANY_FAILED_ATTEMPTS",
            "timeout": timeout
        }), 200
    dbconn = database()
    dbconn.execute("SELECT unix_hash, P.id FROM userpassword UP INNER JOIN people P ON UP.people_id = P.id WHERE P.username = %s", (request.form.get("uname"),))
    results = dbconn.fetchall()
    if not len(results) == 1:
        return "ERR_USERNAME_NOT_UNIQUE", 403
    if passlib.hash.ldap_salted_sha1.verify(request.form.get("passwd"), results[0]["unix_hash"]):
        user = apiUser(results[0]["id"])
        login_user(user)
        pCheck = permissionCheck()
        gMember = groupMembership()
        bf.successfulLogin(request.form.get("uname"))
        return jsonify({
            "status": "SUCCESS",
            "permissions": pCheck.get(current_user.username),
            "groups": gMember.getGroupsOfUser(current_user.username)
        }), 200
    else:
        timeout = bf.failedLogin(request.form.get("uname"))
        return jsonify({
            "status": "ERR_ACCESS_DENIED",
            "timeout": timeout
        }), 401


@loginApi.route("/api/logout", methods=["POST"])
def removeSession():
    logout_user()
    return "SUCCESS", 200


@loginApi.route("/api/login/check", methods=["GET"])
@login_required
def checkSession():
    pCheck = permissionCheck()
    gMember = groupMembership()
    return jsonify({
        "status": "SUCCESS",
        "permissions": pCheck.get(current_user.username),
        "groups": gMember.getGroupsOfUser(current_user.username)
    }), 200
