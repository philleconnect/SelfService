#!/usr/bin/env python3

# SchoolConnect SelfService API
# User API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import requests

# Include modules
import modules.database as db
import helpers.hash as hash

# Endpoint definition
userApi = Blueprint("userApi", __name__)
@userApi.route("/api/user/data", methods=["GET", "PUT"])
@login_required
def myData():
    dbconn = db.database()
    dbconn.execute("SELECT id, username, firstname, lastname, DATE_FORMAT(birthdate, '%d.%m.%Y') AS birthdate, email FROM people WHERE username = %s LIMIT 1", (current_user.username,))
    return jsonify(dbconn.fetchone()), 200

@userApi.route("/api/user/email", methods=["PUT"])
@login_required
def saveEmail(id):
    dbconn = db.database()
    dbconn.execute("UPDATE people SET email = %s WHERE username = %s", (request.form.get("email"), current_user.username))
    if not dbconn.commit():
        return "ERR_DATABASE_ERROR", 500
    return "SUCCESS", 200

@userApi.route("/api/user/password", methods=["PUT"])
@login_required
def updatePassword():
    dbconn = db.database()
    dbconn.execute("SELECT id FROM people WHERE username = %s", (current_user.username,))
    result = dbconn.fetchone()
    if not request.form.get("password1") == request.form.get("password2"):
        return "ERR_PASSWORDS_DIFFERENT", 500
    dbconn.execute("UPDATE userpassword SET unix_hash = %s, smb_hash = %s, hint = %s, autogen = 0, cleartext = NULL WHERE people_id = %s", (hash.unix(request.form.get("password1")), hash.samba(request.form.get("password1")), request.form.get("hint"), result["id"]))
    if not dbconn.commit():
        return "ERR_DATABASE_ERROR", 500
    ldap = requests.post(url = "http://pc_admin/api/public/usercheck/" + result["id"])
    if not ldap.text == "SUCCESS":
        return "ERR_LDAP_ERROR", 500
    return "SUCCESS", 200

@userApi.route("/api/user/resetpassword", methods=["PUT"])
@login_required
def resetPassword():
    dbconn = db.database()
    return None
