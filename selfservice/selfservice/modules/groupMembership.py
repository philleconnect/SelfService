#!/usr/bin/env python3

# SchoolConnect SelfService API
# Group membership checker
# © 2020 - 2021 Johannes Kreutz.

# Include modules
from modules.database import database

# Class definition
class groupMembership:
    def __init__(self):
        self.__dbconn = database()

    # Helper to get groups of user
    def getGroupsOfUser(self, user):
        self.__dbconn.execute("SELECT name FROM groups G INNER JOIN people_has_groups PHG ON G.id = PHG.group_id INNER JOIN people P ON P.id = PHG.people_id WHERE P.username = %s", (user,))
        groups = []
        for group in self.__dbconn.fetchall():
            groups.append(group["name"])
        return groups

    # Check if user belongs to group
    def checkGroupMembership(self, user, group):
        if group in self.getGroupsOfUser(user):
            return True
        return False
