#!/usr/bin/env python3

# SchoolConnect SelfService API
# Course API endpoint
# © 2020 Johannes Kreutz.

# Include dependencies
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import pdfkit
import datetime
import base64

# Include modules
from modules.database import database
from modules.permissionCheck import permissionCheck
import helpers.courselist as cl

# Endpoint definition
courseApi = Blueprint("courseApi", __name__)
@courseApi.route("/api/course/my", methods=["GET"])
@login_required
def getMyCourses():
    dbconn = database()
    dbconn.execute("SELECT G.id, name FROM groups G INNER JOIN people_has_groups PHG ON G.id = PHG.group_id INNER JOIN people P ON P.id = PHG.people_id WHERE P.username = %s AND G.type = 3", (current_user.username,))
    return jsonify(dbconn.fetchall()), 200

@courseApi.route("/api/course/detail/<id>", methods=["GET"])
@login_required
def getCourseDetail(id):
    pCheck = permissionCheck()
    if not "grouplst" in pCheck.get(current_user.username):
        return "ERR_NOT_ALLOWED", 403
    course = {"name": cl.getCourseName(id), "members": cl.getCourseDetails(id)}
    return jsonify(course), 200

@courseApi.route("/api/course/csv/<id>", methods=["GET"])
@login_required
def getCourseCSV(id):
    dbconn = database()
    pCheck = permissionCheck()
    if not "grouplst" in pCheck.get(current_user.username):
        return "ERR_NOT_ALLOWED", 403
    csv = {"name": cl.getCourseName(id), "content": "data:text/csv;charset=utf-8,Vorname;Nachname;E-Mail;Geburtsdatum\n"}
    for member in cl.getCourseDetails(id, True):
        row = member["firstname"] + ";" + member["lastname"] + ";" + member["email"] + ";" + member["birthdate"] + "\n"
        csv["content"] += row
    return jsonify(csv), 200

@courseApi.route("/api/course/pdf/<id>", methods=["GET"])
@login_required
def getCoursePDF(id):
    dbconn = database()
    pCheck = permissionCheck()
    if not "grouplst" in pCheck.get(current_user.username):
        return "ERR_NOT_ALLOWED", 403
    courseName = cl.getCourseName(id)
    pdf = {"name": courseName, "content": "data:application/pdf;base64,"}
    tableCode = ""
    style = False
    for member in cl.getCourseDetails(id):
        name = member["name"] if not member["name"] == "" else "-"
        email = member["email"] if not member["email"] == "" else "-"
        birthdate = member["birthdate"] if not member["birthdate"] == "" else "-"
        cssClass = " class=\"alt\"" if style else ""
        style = not style
        tableCode += "<tr" + cssClass + "><td>" + name + "</td><td>" + email + "</td><td>" + birthdate + "</td></tr>"
    htmlCode = "<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>Kursliste " + courseName + "</title></head><body><h1>Kursliste " + courseName + "</h1><p>Erzeugt am " + datetime.datetime.now().strftime("%d.%m.%Y um %H:%M:%S") + "</p><div class=\"datagrid\"><table><thead><tr><th style=\"background-color:#1155B9;\">Name</th><th>E-Mail</th><th>Geburtsdatum</th></tr></thead><tbody></tbody>" + tableCode + "</table></div><p>PDF-Datei erzeugt mit PhilleConnect.</p></body></html>"
    options = {
        "page-size": "A4",
        "margin-top": "0.25in",
        "margin-right": "0.5in",
        "margin-bottom": "0.25in",
        "margin-left": "0.5in",
        "encoding": "UTF-8",
        "title": "Kursliste " + courseName
    }
    pdfCode = pdfkit.from_string(htmlCode, False, options=options, css="/usr/local/bin/selfservice/pdf.css")
    pdf["content"] += base64.b64encode(pdfCode).decode("UTF-8")
    return jsonify(pdf), 200
