#!/usr/bin/env python3

# SchoolConnect SelfService API
# API User class
# © 2020 Johannes Kreutz.

# Include dependencies
from flask_login import UserMixin

# Include modules
import modules.database as db

# Class definition
class apiUser(UserMixin):
    def __init__(self, id):
        self.id = id
        dbconn = db.database()
        dbconn.execute("SELECT username FROM people WHERE id = %s", (id,))
        result = dbconn.fetchone()
        self.username = result["username"]
