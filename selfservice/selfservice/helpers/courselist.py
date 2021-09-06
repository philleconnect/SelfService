#!/usr/bin/env python3

# SchoolConnect SelfService API
# Course list functions
# © 2020 - 2021 Johannes Kreutz.


# Include modules
from modules.database import database


# Course list helper functions
def getCourseDetails(id, separateNames=False):
    dbconn = database()
    if separateNames:
        dbconn.execute("SELECT lastname, firstname, email, DATE_FORMAT(birthdate, '%d.%m.%Y') AS birthdate FROM people P INNER JOIN people_has_groups PHG ON P.id = PHG.people_id INNER JOIN groups G ON G.id = PHG.group_id WHERE G.id = %s ORDER BY lastname, firstname", (id,))
    else:
        dbconn.execute("SELECT preferredname AS name, lastname, firstname, email, DATE_FORMAT(birthdate, '%d.%m.%Y') AS birthdate FROM people P INNER JOIN people_has_groups PHG ON P.id = PHG.people_id INNER JOIN groups G ON G.id = PHG.group_id WHERE G.id = %s ORDER BY lastname, firstname", (id,))
    return dbconn.fetchall()


def getCourseName(id):
    dbconn = database()
    dbconn.execute("SELECT name FROM groups WHERE id = %s", (id,))
    return dbconn.fetchone()["name"]
