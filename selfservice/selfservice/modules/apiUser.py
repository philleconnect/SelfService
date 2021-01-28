#!/usr/bin/env python3

# SchoolConnect SelfService API
# API User class
# © 2020 - 2021 Johannes Kreutz.

# Include dependencies
from flask_login import UserMixin

# Include modules
from modules.database import database

# Class definition
class apiUser(UserMixin):
    def __init__(self, id):
        self.id = id
        dbconn = database()
        dbconn.execute("SELECT username FROM people WHERE id = %s", (id,))
        result = dbconn.fetchone()
        self.username = result["username"]
