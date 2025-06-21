"""Functions to find the local project config, if one exists"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

import os.path as os_path
from os.path import dirname
from timetracker.consts import DIRTRK


class CfgFinder:
    """Functionality to find the local project config, if one is present"""

    def __init__(self, dircur, trksubdir=None):
        self.dircur = dircur
        self.trksubdir = trksubdir if trksubdir is not None else DIRTRK
        # Existing directory (ex: ./timetracker) or None if dir not exist
        self.dirtrk = _get_abspathtrk(dircur, self.trksubdir)
        self.dirgit = _get_abspathtrk(dircur, '.git')
        # Get the project tracking directory that is or will be tracked
        self.dirtrk_pathname = self._init_dirtrk()
        self.dirproj = dirname(self.dirtrk_pathname)
        self.project = self._init_project()

    def get_dirtrk(self):
        """Get the project tracking directory that is or will be tracked"""
        return self.dirtrk_pathname

    def get_dirgit(self):
        """Get the .git directory if it is the current dir or any parents"""
        return _get_abspathtrk(self.dircur, '.git')

    def get_cfgfilename(self):
        """Get the local (aka project) config full filename"""
        return os_path.join(self.dirtrk_pathname, 'config')

    def get_dircsv_default(self):
        """Get the default csv directory for use in the cli help string.

               is_present(dirtrk)
                 is_present(dirgit)
                              00|01|11|10
                             +--+--+--+--
                           0 | X| P| P| P
          dircur==dirproj    +--+--+--+--
                           1 | .| .| .| .
                             +--+--+--+--
        Not using in default value
        """
        if os_path.realpath(self.dircur) == os_path.realpath(self.dirproj):
            return '.'
        assert not (self.dirtrk is None and self.dirgit is None)
        return self.dirproj

    def get_dirproj(self):
        """Get the project directory"""
        return dirname(self.dirtrk_pathname)

    def get_dircur_rel(self):
        """Get the current directory relative to the project directory"""
        return os_path.relpath(self.dircur, self.get_dirproj())

    def get_desc(self):
        """Get a description of the state of a CfgFinder instance"""
        dirgit = self.get_dirgit()
        return (f'CfgFinder project({self.project}) '
                f'dircur({self.get_dircur_rel()})\n'
                f'CfgFinder dircur:      {self.dircur}\n'
                f'CfgFinder get_dirtrk:  {self.dirtrk_pathname}\n'
                f'CfgFinder dirproj:     {self.dirproj}\n'
                f'CfgFinder dirtrk:      {self.dirtrk}\n'
                f'CfgFinder dirgit:      {dirgit}\n'
                f'CfgFinder dircsv_dflt: {self.get_dircsv_default()}')

    def _init_project(self):
        dirtrk = self.dirtrk_pathname if self.dirtrk is None else self.dirtrk
        return os_path.basename(dirname(dirtrk))

    def _init_dirtrk(self):
        """Get the project tracking directory that is or will be tracked"""
        if self.dirtrk is not None:
            return self.dirtrk
        dirgit = self.get_dirgit()
        if dirgit is not None:
            return os_path.normpath(os_path.join(dirname(dirgit), self.trksubdir))
        return os_path.normpath(os_path.join(self.dircur, self.trksubdir))


def _get_abspathtrk(path, trksubdir):
    """Get .timetracker/ proj dir by searching up parent path"""
    trkabsdir, found = _finddirtrk(path, trksubdir)
    return trkabsdir if found else None

def _finddirtrk(path, trksubdir):
    """Walk up dirs until find .timetracker/ proj dir or mount dir"""
    path = os_path.abspath(path)
    join = os_path.join
    trkdir = join(path, trksubdir)
    exists = os_path.exists
    if exists(trkdir):
        return os_path.normpath(trkdir), True
    ismount = os_path.ismount
    while not ismount(path):
        trkdir = join(path, trksubdir)
        if exists(trkdir):
            return os_path.normpath(trkdir), True
        path = dirname(path)
    return os_path.normpath(path), False


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
