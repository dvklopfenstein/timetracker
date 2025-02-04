"""Functions to find the local project config, if one exists"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import environ
from os.path import exists
from os.path import abspath
from os.path import dirname
from os.path import join
from os.path import ismount
from os.path import basename
from os.path import normpath
from logging import debug
from timetracker.consts import DIRTRK


class CfgFinder:
    """Functionality to find the local project config, if one exists"""

    def __init__(self, dircur, trksubdir=None):
        self.dircur = dircur
        self.trksubdir = trksubdir if trksubdir is not None else DIRTRK
        # Existing directory (ex: ./timetracker) or None if dir not exist
        self.dirtrk = get_abspathtrk(dircur, self.trksubdir)
        self.project = self._init_project()

    def get_dirtrk(self):
        """Get the project directory that is or will be tracked"""
        if self.dirtrk is not None:
            return self.dirtrk
        return normpath(join(self.dircur, self.trksubdir))

    def get_cfgfilename(self):
        """Get the local (aka project) config full filename"""
        return join(self.get_dirtrk(), 'config')

    def __str__(self):
        return ('CfgFinder('
                f'project={self.project}, '
                f'dirtrk={self.dirtrk}, '
                f'dircur={self.dircur})')

    def _init_project(self):
        debug(f'CfgFinder PPPPPPPPPPPPPPPPPPPPPPPPPP self.dirtrk {self.dirtrk}')
        debug(f'CfgFinder PPPPPPPPPPPPPPPPPPPPPPPPPP CURRENT DIR {self.dircur}')
        if self.dirtrk is not None:
            return basename(dirname(self.dirtrk))
        return basename(self.dircur)


def get_username(name=None):
    """Get the default username"""
    if name is None:
        return environ.get('USER', 'researcher')
    if name in environ:
        return environ[name]
    return name


def get_abspathtrk(path, trksubdir):
    """Get .timetracker/ proj dir by searching up parent path"""
    ##debug(f'CfgFinder path       {path}')
    trkabsdir, found = finddirtrk(path, trksubdir)
    return trkabsdir if found else None

def finddirtrk(path, trksubdir):
    """Walk up dirs until find .timetracker/ proj dir or mount dir"""
    path = abspath(path)
    trkdir = join(path, trksubdir)
    if exists(trkdir):
        ##debug(f'CfgFinder path       {path}')
        return normpath(trkdir), True
    while not ismount(path):
        ##debug(f'PATHWALK: {path}')
        trkdir = join(path, trksubdir)
        if exists(trkdir):
            return normpath(trkdir), True
        path = dirname(path)
    return normpath(path), False


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
