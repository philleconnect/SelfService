#!/usr/bin/env python3

# SchoolConnect SelfService API
# Password email reset API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import requests
import passlib.hash
import datetime
import os

# Include modules
import modules.database as db
import helpers.hash as hash
import helpers.resetEmail as email
import helpers.essentials as es
import modules.permissionCheck as pc

# Endpoint definition
resetApi = Blueprint("resetApi", __name__)
@resetApi.route("/api/reset/start", methods=["PUT"])
def createResetSession():
    isResetEnabled = os.environ.get("EMAIL_RESET_ENABLED")
    if not isResetEnabled.lower() == "true":
        return "ERR_SERVICE_DISABLED", 500
    dbconn = db.database()
    dbconn.execute("SELECT COUNT(*) AS num, id, email, firstname FROM people WHERE username = %s", (request.form.get("username"),))
    result = dbconn.fetchone()
    if not result["num"] == 1:
        return "ERR_USER_NOT_FOUND", 500
    pCheck = pc.permissionCheck()
    permissions = pCheck.get(request.form.get("username"))
    if not "emailrst" in permissions:
        return "ERR_NOT_ALLOWED", 500
    if not request.form.get("password1") == request.form.get("password2"):
        return "ERR_PASSWORDS_DIFFERENT", 500
    if result["email"] == "" or result["email"] == None:
        return "ERR_NO_EMAIL", 500
    dbconn.execute("SELECT COUNT(*) AS num, time FROM mailreset WHERE people_id = %s", (result["id"],))
    oldTokens = dbconn.fetchone()
    if oldTokens["num"] > 0:
        earliestCreation = datetime.datetime.now() - datetime.timedelta(days=1)
        if oldTokens["time"] >= earliestCreation:
            return "ERR_OPEN_RESET_REQUEST", 500
        else:
            dbconn.execute("DELETE FROM mailreset WHERE people_id = %s", (result["id"],))
            if not dbconn.commit():
                return "ERR_DATABASE_ERROR", 500
    token = es.randomString(128)
    dbconn.execute("INSERT INTO mailreset (time, token, people_id, unix_hash, smb_hash) VALUES (NOW(), %s, %s, %s, %s)", (token, result["id"], hash.unix(request.form.get("password1")), hash.samba(request.form.get("password1"))))
    if not dbconn.commit():
        return "ERR_DATABASE_ERROR", 500
    mailstatus = email.sendResetEmail(result["email"], token, result["firstname"])
    if mailstatus == -1:
        return "ERR_SMTP_CONNECTION_REFUSED", 500
    elif mailstatus == -2:
        return "ERR_SMTP_CREDENTIALS_ERROR", 500
    elif mailstatus <= -3:
        return "ERR_OTHER_SMTP_ERROR", 500
    return "SUCCESS", 200

@resetApi.route("/api/reset/confirm/<token>", methods=["POST"])
def confirmReset(token):
    dbconn = db.database()
    dbconn.execute("SELECT COUNT(*) AS num, unix_hash, smb_hash, time, people_id AS id FROM mailreset WHERE token = %s", (token,))
    result = dbconn.fetchone()
    if not result["num"] == 1:
        return "ERR_TOKEN_NOT_FOUND", 500
    earliestCreation = datetime.datetime.now() - datetime.timedelta(days=1)
    if result["time"] < earliestCreation:
        return "ERR_TIMEOUT", 200
    dbconn.execute("UPDATE userpassword SET unix_hash = %s, smb_hash = %s WHERE people_id = %s", (result["unix_hash"], result["smb_hash"], result["id"]))
    dbconn.execute("DELETE FROM mailreset WHERE token = %s", (token,))
    if not dbconn.commit():
        return "ERR_DATABASE_ERROR", 500
    ldap = requests.post(url = "http://pc_admin/api/public/usercheck/" + result["id"])
    if not ldap.text == "SUCCESS":
        return "ERR_LDAP_ERROR", 500
    return "SUCCESS", 200
