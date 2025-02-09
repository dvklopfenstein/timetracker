"""Functions to find the local project config, if one exists"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from os.path import relpath
from os.path import abspath
from os.path import dirname
from os.path import join
from os.path import ismount
from os.path import basename
from os.path import normpath
from logging import debug
from timetracker.consts import DIRTRK
from timetracker.cfg.cfg_local import CfgProj


class CfgFinder:
    """Functionality to find the local project config, if one exists"""

    def __init__(self, dircur, trksubdir=None):
        self.dircur = dircur
        self.trksubdir = trksubdir if trksubdir is not None else DIRTRK
        # Existing directory (ex: ./timetracker) or None if dir not exist
        self.dirtrk = get_abspathtrk(dircur, self.trksubdir)
        # Get the project tracking directory that is or will be tracked
        self.dirgit = get_abspathtrk(dircur, '.git')
        self.dirtrk_pathname = self._init_dirtrk()
        self.project = self._init_project()

    def get_dirtrk(self):
        """Get the project tracking directory that is or will be tracked"""
        return self.dirtrk_pathname

    def get_cfgfilename(self):
        """Get the local (aka project) config full filename"""
        return join(self.dirtrk_pathname, 'config')

    def get_dircsv(self):
        """Get the csv directory name"""
        fname = self.get_cfgfilename()
        cfg = CfgProj(fname)
        return cfg.dircsv

    def get_csvfilename(self):
        """Get the csv filename pointed to in the .timetracker/config file"""
        fname = self.get_cfgfilename()
        if exists(fname):
            cfg = CfgProj(fname)
            csvname = cfg.get_filename_csv()
            debug(f'CCCCCCCCCCCCCCCCSSSSSSSSSSSSSSSVVVVVVVVVVVVVVV: {csvname}')
            return csvname
        return None

    def get_dirproj(self):
        """Get the project directory"""
        return dirname(self.dirtrk_pathname)

    def get_dircur_rel(self):
        """Get the current directory relative to the project directory"""
        return relpath(self.dircur, self.get_dirproj())

    def get_desc(self):
        """Get a description of the state of a CfgFinder instance"""
        return (f'CfgFinder project({self.project}) '
                f'dircur({self.get_dircur_rel()})\n'
                f'CfgFinder dircur:     {self.dircur}\n'
                f'CfgFinder get_dirtrk: {self.dirtrk_pathname}\n'
                f'CfgFinder dirtrk:     {self.dirtrk}\n'
                f'CfgFinder dirgit:     {self.dirgit}')

    def _init_project(self):
        dirtrk = self.dirtrk_pathname if self.dirtrk is None else self.dirtrk
        return basename(dirname(dirtrk))

    def _init_dirtrk(self):
        """Get the project tracking directory that is or will be tracked"""
        if self.dirtrk is not None:
            return self.dirtrk
        if self.dirgit is not None:
            return normpath(join(dirname(self.dirgit), self.trksubdir))
        return normpath(join(self.dircur, self.trksubdir))

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
