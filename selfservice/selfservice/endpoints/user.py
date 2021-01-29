#!/usr/bin/env python3

# SchoolConnect SelfService API
# User API endpoint
# © 2020 - 2021 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import requests
import passlib.hash

# Include modules
from modules.permissionCheck import permissionCheck
from modules.database import database
from modules.groupMembership import groupMembership
import helpers.hash as hash

# Endpoint definition
userApi = Blueprint("userApi", __name__)
@userApi.route("/api/user/data", methods=["GET"])
@login_required
def myData():
    dbconn = database()
    dbconn.execute("SELECT id, username, firstname, lastname, DATE_FORMAT(birthdate, '%d.%m.%Y') AS birthdate, email FROM people WHERE username = %s LIMIT 1", (current_user.username,))
    return jsonify(dbconn.fetchone()), 200

@userApi.route("/api/user/email", methods=["POST"])
@login_required
def saveEmail():
    dbconn = database()
    dbconn.execute("UPDATE people SET email = %s WHERE username = %s", (request.form.get("email"), current_user.username))
    if not dbconn.commit():
        return "ERR_DATABASE_ERROR", 500
    dbconn.execute("SELECT id FROM people WHERE username = %s", (current_user.username,))
    result = dbconn.fetchone()
    ldap = requests.post(url = "http://pc_admin/api/public/usercheck/" + result["id"])
    if not ldap.text == "SUCCESS":
        return "ERR_LDAP_ERROR", 500
    return "SUCCESS", 200

@userApi.route("/api/user/password", methods=["POST"])
@login_required
def updatePassword():
    dbconn = database()
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

@userApi.route("/api/user/resetlist", methods=["GET"])
@login_required
def listUsers():
    gMember = groupMembership()
    if not gMember.checkGroupMembership(current_user.username, "teachers"):
        return "ERR_NOT_ALLOWED", 403
    dbconn = database()
    dbconn.execute("SELECT P.id, preferredname, username FROM people P INNER JOIN people_has_groups PHG ON PHG.people_id = P.id INNER JOIN groups G ON G.id = PHG.group_id INNER JOIN groups_has_permission GHP ON GHP.group_id = G.id INNER JOIN permission PM ON PM.id = GHP.permission_id WHERE PM.detail = 'pwalwrst' ORDER BY username")
    users = []
    for user in dbconn.fetchall():
        users.append({"id":user["id"],"name":user["preferredname"] + " (" + user["username"] + ")"})
    return jsonify(users), 200

@userApi.route("/api/user/resetpassword/<id>", methods=["POST"])
@login_required
def resetPassword(id):
    gMember = groupMembership()
    if not gMember.checkGroupMembership(current_user.username, "teachers"):
        return "ERR_NOT_ALLOWED", 403
    dbconn = database()
    pCheck = permissionCheck()
    permissions = pCheck.getForId(id)
    if not "pwalwrst" in permissions:
        return "ERR_NOT_ALLOWED", 403
    dbconn.execute("SELECT id FROM people WHERE username = %s", (current_user.username,))
    teacherResult = dbconn.fetchone()
    dbconn.execute("SELECT unix_hash FROM userpassword WHERE people_id = %s", (teacherResult["id"],))
    teacherPasswordResult = dbconn.fetchone()
    if not passlib.hash.ldap_salted_sha1.verify(request.form.get("passwd"), teacherPasswordResult["unix_hash"]):
        return "ERR_ACCESS_DENIED", 401
    if not request.form.get("password1") == request.form.get("password2"):
        return "ERR_PASSWORDS_DIFFERENT", 500
    dbconn.execute("UPDATE userpassword SET unix_hash = %s, smb_hash = %s, hint = %s, autogen = 0, cleartext = NULL WHERE people_id = %s", (hash.unix(request.form.get("password1")), hash.samba(request.form.get("password1")), request.form.get("hint"), id))
    if not dbconn.commit():
        return "ERR_DATABASE_ERROR", 500
    ldap = requests.post(url = "http://pc_admin/api/public/usercheck/" + id)
    if not ldap.text == "SUCCESS":
        return "ERR_LDAP_ERROR", 500
    return "SUCCESS", 200
