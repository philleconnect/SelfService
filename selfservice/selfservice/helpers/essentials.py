#!/usr/bin/env python3

# SchoolConnect SelfService API
# Essential functions
# © 2020 - 2021 Johannes Kreutz.


# Include dependencies
import os
import random
from flask_login import current_user


# Include modules
from modules.permissionCheck import permissionCheck


# Essential functions
def randomString(length=10):
    letters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join(random.choice(letters) for i in range(length))


def isAuthorized(permissions):
    permissionCheck = permissionCheck()
    return permissionCheck.check(current_user.username, permissions)
