#!/usr/bin/env python3
"""Base class for object that runs tests"""


class RunBase:
    """Base class for object that runs tests"""
    # pylint: disable=too-few-public-methods

    def __init__(self, project, username, dircur, dirgit01):
        self.project = project
        self.uname = username
        self.dircurattr = dircur
        self.dirgit01 = dirgit01
