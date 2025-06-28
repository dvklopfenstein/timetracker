"""Local project configuration parser for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

import os
import os.path as op
import datetime
from timetracker import consts


# 2025-01-21 17:09:47.035936

class Starttime:
    """Local project configuration parser for timetracking"""

    min_trigger = datetime.timedelta(hours=10)

    def __init__(self, dircfg, project, name):
        self.dircfg  = op.abspath(consts.DIRTRK) if dircfg is None else op.normpath(dircfg)
        self.project = project
        self.name = name
        self.filename = op.join(self.dircfg, f'start_{project}_{name}.txt')

    def started(self):
        """Return True if the timer is starte, False if not"""
        return op.exists(self.filename)

    def wr_starttime(self, starttime, activity=None, tags=None):
        """Write the start time into a ./timetracker/start_*.txt"""
        assert starttime is not None
        with open(self.filename, 'w', encoding='utf8') as prt:
            ststr = starttime.strftime(consts.FMTDT)
            prt.write(f'{ststr}')
            if activity:
                prt.write(f'\nAC {activity}')
            if tags:
                for tag in tags:
                    prt.write(f'\nTG {tag}')
            return

    def get_desc(self, note=' set'):
        """Get a string describing the state of an instance of the CfgProj"""
        return (
            f'CfgProj {note} {int(op.exists(self.filename))} '
            f'fname start {self.filename}')

    def rm_starttime(self):
        """Remove the starttime file, thus resetting the timer"""
        fstart = self.filename
        if op.exists(fstart):
            os.remove(fstart)

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
                    return datetime.datetime.strptime(line, consts.FMTDT)
        return None

    def hms_from_startfile(self, dtstart):
        """Get the elapsed time starting from time in a starttime file"""
        return datetime.datetime.now() - dtstart if dtstart is not None else None

    def str_elapsed_hms(self, hms, msg):
        """Get a string describing the elapsed time"""
        return f"{msg} H:M:S {hms} for '{self.project}' ID={self.name}"


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
