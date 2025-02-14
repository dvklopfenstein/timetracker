"""Local project configuration parser for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import remove
from os.path import exists
from os.path import basename
from os.path import join
from os.path import abspath
from os.path import dirname
from os.path import normpath
from datetime import datetime
from logging import debug

from timetracker.utils import orange
from timetracker.consts import DIRTRK
from timetracker.cfg.utils import get_username

# 2025-01-21 17:09:47.035936
FMTDT = '%Y-%m-%d %H:%M:%S.%f'


class Starttime:
    """Local project configuration parser for timetracking"""

    CSVPAT = 'timetracker_PROJECT_$USER$.csv'

    def __init__(self, dircfg, project=None, name=None):
        debug(orange(f'Starttime args {int(exists(dircfg))} dircfg {dircfg}'))
        debug(f'Starttime args . project  {project}')
        debug(f'Starttime args . name     {name}')
        self.dircfg  = abspath(DIRTRK) if dircfg is None else normpath(dircfg)
        self.project = basename(dirname(self.dircfg)) if project is None else project
        self.name = get_username(name) if name is None else name

    def get_desc(self, note=' set'):
        """Get a string describing the state of an instance of the CfgProj"""
        return (
            f'CfgProj {note} {int(exists(self.get_filename_start()))} '
            f'fname start {self.get_filename_start()}')

    def get_filename_start(self):
        """Get the file storing the start time a person"""
        fstart = join(self.dircfg, f'start_{self.project}_{self.name}.txt')
        debug(f'CFG LOCAL: STARTFILE exists({int(exists(fstart))}) {fstart}')
        return fstart

    def read_starttime(self):
        """Read the start time file"""
        fname = self.get_filename_start()
        return _read_starttime(fname)

    def prt_elapsed(self):
        """Print elapsed time if timer is started"""
        fin_start = self.get_filename_start()
        # Print elapsed time, if timer was started
        if exists(fin_start):
            hms = hms_from_startfile(fin_start)
            print(f'Timer running: {hms} H:M:S '
                  f"elapsed time for '{self.project}' ID={self.name}")

    def rm_starttime(self):
        """Remove the starttime file, thus resetting the timer"""
        fstart = self.get_filename_start()
        if exists(fstart):
            remove(fstart)

def hms_from_startfile(fname):
    """Get the elapsed time starting from time in a starttime file"""
    dtstart = _read_starttime(fname)
    return datetime.now() - dtstart if dtstart is not None else None

def _read_starttime(fname):
    """Get datetime from a starttime file"""
    if exists(fname):
        with open(fname, encoding='utf8') as ifstrm:
            for line in ifstrm:
                line = line.strip()
                assert len(line) == 26  # "2025-01-22 04:05:00.086891"
                return datetime.strptime(line, FMTDT)
    return None


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
