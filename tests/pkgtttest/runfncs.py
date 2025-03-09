#!/usr/bin/env python3
"""Base class for object that runs tests"""

from os.path import exists
from timetracker.cfg.finder import CfgFinder
from tests.pkgtttest.mkprojs import mk_projdirs
from tests.pkgtttest.mkprojs import findhome_str


class RunBase:
    """Base class for object that runs tests"""
    # pylint: disable=too-few-public-methods

    def __init__(self, project, username, dircur, dirgit01):
        self.project = project
        self.uname = username
        self.dircur = dircur
        self.dirgit01 = dirgit01


def proj_setup(tmphome, project, dircur, dirgit01=True):
    """After creating a tmphome using TemporaryDirectory, create these"""
    exp = mk_projdirs(tmphome, project, dirgit01)
    finder = CfgFinder(dircur=getattr(exp, dircur), trksubdir=None)
    cfgname = finder.get_cfgfilename()
    assert not exists(cfgname), findhome_str(exp.dirhome)
    return cfgname, finder, exp
