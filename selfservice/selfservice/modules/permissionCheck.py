#!/usr/bin/env python3

# SchoolConnect SelfService API
# Permission checker
# © 2020 Johannes Kreutz.

# Include modules
import modules.database as db

# Class definition
class permissionCheck:
    def __init__(self):
        self.__dbconn = db.database()

    # Helper to get permissions of user
    def __getPermissionsOfUser(self, user):
        self.__dbconn.execute("SELECT P.detail AS detail FROM permission P INNER JOIN groups_has_permission GHP ON GHP.permission_id = P.id INNER JOIN groups G ON G.id = GHP.group_id INNER JOIN people_has_groups PEHG ON PEHG.group_id = G.id INNER JOIN people PE ON PE.id = PEHG.people_id WHERE PE.username = %s", (user,))
        return self.__dbconn.fetchall()

    # Check if user has wanted permission
    def check(self, user, wanted):
        if not isinstance(wanted, list):
            wanted = [wanted]
        for permission in wanted:
            for has in self.__getPermissionsOfUser(user):
                if has["detail"] == permission:
                    return True
        return False

    # Return array with permissions
    def get(self, user):
        p = []
        for has in self.__getPermissionsOfUser(user):
            p.append(has["detail"])
        return p

    # List all permissions for a user id
    def getForId(self, id):
        self.__dbconn.execute("SELECT username FROM people WHERE id = %s LIMIT 1", (id,))
        username = self.__dbconn.fetchone()["username"]
        return self.get(username)
