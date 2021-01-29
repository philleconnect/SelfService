#!/usr/bin/env python3

# SchoolConnect SelfService API
# Brute force protection class
# © 2020 - 2021 Johannes Kreutz.


# Include dependencies
from redis import Redis
import datetime
import json


# Class definition
class bruteforceProtection:
    steps = [10, 30, 60, 300, 600, 3600]

    def __init__(self):
        self.__r = Redis(host="selfservice-redis")

    # A failed login has taken place. Update blocker and return waiting time
    def failedLogin(self, username):
        if not self.__r.exists(username):
            newIndex = 0
        else:
            value = json.loads(self.__r.get(username))
            index = self.steps.index(value["blockedFor"])
            newIndex = index + 1 if len(self.steps) - 1 > index else 5
        self.__r.set(username, json.dumps({
            "timestamp": datetime.datetime.now().timestamp(),
            "blockedFor": self.steps[newIndex]
        }))
        return self.steps[newIndex]

    # A successful login, remove blocker
    def successfulLogin(self, username):
        self.__r.delete(username)

    # Check if the username is currently blocked
    def isBlocked(self, username):
        if not self.__r.exists(username):
            return 0
        else:
            value = json.loads(self.__r.get(username))
            compare = datetime.datetime.fromtimestamp(value["timestamp"]) + datetime.timedelta(seconds = value["blockedFor"])
            if compare < datetime.datetime.now():
                return 0
            return (compare - datetime.datetime.now()).total_seconds()
