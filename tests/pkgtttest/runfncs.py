#!/usr/bin/env python3
"""Base class for object that runs tests"""

from os.path import isabs
from os.path import exists
from timetracker.cfg.finder import CfgFinder
from tests.pkgtttest.mkprojs import mk_projdirs


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
    ntexpdirs = mk_projdirs(tmphome, project, dirgit01)
    finder = CfgFinder(dircur=getattr(ntexpdirs, dircur), trksubdir=None)
    fcfgproj = finder.get_cfgfilename()
    #assert not exists(fcfgproj), findhome_str(exp.dirhome)
    return fcfgproj, finder, ntexpdirs


def prt_expdirs(ntexpdirs, name=""):
    """Print the expected directories and files and if they exist"""
    for key, expdir in ntexpdirs._asdict().items():
        print(f'{name} '
              f'exists({int(exists(expdir)) if expdir is not None and isabs(expdir) else "."}) '
              f'{key:14} {expdir}')
