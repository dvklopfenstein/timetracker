#!/usr/bin/env python3
"""Test the location of the csv file"""


class TestBase:
    """Base class for test object"""
    # pylint: disable=too-few-public-methods

    def __init__(self, project, username, dircur, dirgit01):
        self.project = project
        self.uname = username
        self.dircurattr = dircur
        self.dirgit01 = dirgit01
