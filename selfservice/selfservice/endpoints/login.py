#!/usr/bin/env python3

# SchoolConnect SelfService API
# Login API endpoint
# © 2020 - 2021 Johannes Kreutz.


# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user
import passlib.hash


# Include modules
from modules.database import database
from modules.apiUser import apiUser
from modules.permissionCheck import permissionCheck
from modules.groupMembership import groupMembership


# Endpoint definition
loginApi = Blueprint("loginApi", __name__)


@loginApi.route("/api/login", methods=["POST"])
def createSession():
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
        return jsonify({
            "permissions": pCheck.get(current_user.username),
            "groups": gMember.getGroupsOfUser(current_user.username)
        }), 200
    else:
        return "ERR_ACCESS_DENIED", 401


@loginApi.route("/api/logout", methods=["POST"])
def removeSession():
    logout_user()
    return "SUCCESS", 200
