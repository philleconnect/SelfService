#!/usr/bin/env python3

# SchoolConnect SelfService API
# Course API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

# Include modules
import modules.database as db
import modules.permissionCheck as pc

# Endpoint definition
courseApi = Blueprint("courseApi", __name__)
@courseApi.route("/api/course/my", methods=["GET"])
@login_required
def getMyCourses():
    dbconn = db.database()
    dbconn.execute("SELECT G.id, name FROM groups G INNER JOIN people_has_groups PHG ON G.id = PHG.group_id INNER JOIN people P ON P.id = PHG.people_id WHERE P.username = %s AND G.type = 3", (current_user.username,))
    return jsonify(dbconn.fetchall()), 200

@courseApi.route("/api/course/detail/<id>", methods=["GET"])
@login_required
def getCourseDetail(id):
    dbconn = db.database()
    pCheck = pc.permissionCheck()
    if not "grouplst" in pCheck.get(current_user.username):
        return "ERR_NOT_ALLOWED", 403
    course = {}
    dbconn.execute("SELECT name FROM groups WHERE id = %s", (id,))
    course["name"] = dbconn.fetchone()["name"]
    dbconn.execute("SELECT preferredname AS name, email, DATE_FORMAT(birthdate, '%d.%m.%Y') AS birthdate FROM people P INNER JOIN people_has_groups PHG ON P.id = PHG.people_id INNER JOIN groups G ON G.id = PHG.group_id WHERE G.id = %s ORDER BY name", (id,))
    course["members"] = dbconn.fetchall()
    return jsonify(course), 200
