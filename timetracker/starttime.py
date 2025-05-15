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
from datetime import timedelta
from logging import debug

from timetracker.utils import orange
from timetracker.consts import DIRTRK
from timetracker.consts import FMTDT
from timetracker.consts import FMTDT_H
from timetracker.cfg.utils import get_username

# 2025-01-21 17:09:47.035936


class Starttime:
    """Local project configuration parser for timetracking"""

    min_trigger = timedelta(hours=5)

    def __init__(self, dircfg, project=None, name=None):
        self.dircfg  = abspath(DIRTRK) if dircfg is None else normpath(dircfg)
        self.project = basename(dirname(self.dircfg)) if project is None else project
        self.name = get_username(name) if name is None else name
        self.filename = join(self.dircfg, f'start_{self.project}_{self.name}.txt')
        debug(orange(f'Starttime args {int(exists(dircfg))} dircfg {dircfg}'))
        debug(f'Starttime args . project  {project}')
        debug(f'Starttime args . name     {name}')
        debug(f'Starttime var  {int(exists(self.filename))} name     {self.filename}')

    def wr_starttime(self, starttime, activity=None, tags=None):
        """Write the start time into a ./timetracker/start_*.txt"""
        if starttime is not None:
            with open(self.filename, 'w', encoding='utf8') as prt:
                prt.write(f'{starttime.strftime(FMTDT)}')
                if activity:
                    prt.write(f'\nAC {activity}')
                if tags:
                    for tag in tags:
                        prt.write(f'\nTG {tag}')
                debug(f'  WROTE START: {starttime.strftime(FMTDT)}')
                debug(f'  WROTE FILE:  {self.filename}')
                return
        raise RuntimeError("NOT WRITING START TIME; NO START TIME FOUND")

    def get_desc(self, note=' set'):
        """Get a string describing the state of an instance of the CfgProj"""
        return (
            f'CfgProj {note} {int(exists(self.filename))} '
            f'fname start {self.filename}')

    def rm_starttime(self):
        """Remove the starttime file, thus resetting the timer"""
        fstart = self.filename
        if exists(fstart):
            remove(fstart)

    def read_starttime(self):
        """Read the starttime"""
        error = None
        try:
            fptr = open(self.filename, encoding='utf8')
        except (FileNotFoundError, PermissionError, OSError) as err:
            error = err
        else:
            with fptr:
                for line in fptr:
                    line = line.strip()
                    assert len(line) == 26, \
                        f'len({line})={len(line)}; EXPFMT: 2025-01-22 04:05:00.086891'
                    assert error is None
                    return datetime.strptime(line, FMTDT)
        return None

    def hms_from_startfile(self, dtstart):
        """Get the elapsed time starting from time in a starttime file"""
        return datetime.now() - dtstart if dtstart is not None else None

    def str_elapsed_hms(self, hms, msg):
        """Get a string describing the elapsed time"""
        return f"{msg} H:M:S {hms} for '{self.project}' ID={self.name}"

    def str_started_n_running(self, dta, hms):
        """Return a string detailing how long the timer has been running"""
        msg = self.str_elapsed_hms(
              hms,
              f'Timer started on {dta.strftime(FMTDT_H)} and running')
        print(msg)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
