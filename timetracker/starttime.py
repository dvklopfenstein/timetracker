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
from timetracker.utils import prt_todo
from timetracker.consts import DIRTRK
from timetracker.consts import FMTDT
from timetracker.consts import FMTDT_H
from timetracker.cfg.utils import get_username
from timetracker.msgs import str_tostart_epoch
from timetracker.msgs import str_how_to_stop_now
from timetracker.msgs import str_started_epoch
from timetracker.msgs import str_not_running
from timetracker.msgs import str_no_time_recorded
from timetracker.epoch import str_arg_epoch

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

    def file_exists(self):
        """Retrun True if starttime file exists, False otherwise"""
        return exists(self.filename)

    def prtmsg_started_csv(self, fcsv):
        """Print message depending on if a csv file containing elapsed time exists"""
        if self.file_exists():
            self.prtmsg_started01()
        else:
            print(str_no_time_recorded(fcsv))

    def prtmsg_started01(self):
        """Print message depending if timer is started or not"""
        assert exists(self.filename), f'FILE MUST EXIST prtmsg_started01: {self.filename}'
        dtstart = self._read_starttime()
        hms = self._hms_from_startfile(dtstart)
        hms1 = hms is not None
        if hms1 and hms <= self.min_trigger:
            self._prtmsg_basic(hms, 'Timer running')
        elif hms1:
            self._prtmsg_triggered(hms, dtstart)
        else:
            prt_todo('TODO: STARTFILE WITH NO HMS')

    def wr_starttime(self, starttime):
        """Write the start time into a ./timetracker/start_*.txt"""
        with open(self.filename, 'w', encoding='utf8') as prt:
            prt.write(f'{starttime.strftime(FMTDT)}')
            debug(f'  WROTE START: {starttime.strftime(FMTDT)}')
            debug(f'  WROTE FILE:  {self.filename}')

    def _prtmsg_basic(self, hms, msg):
        self._prt_elapsed_hms(hms, msg)
        print(str_how_to_stop_now())

    def _prtmsg_triggered(self, hms, dtstart):
        msg = f'Timer started on {dtstart.strftime(FMTDT_H)} and running'
        self._prt_elapsed_hms(hms, msg)
        print(str_started_epoch())
        print(str_arg_epoch(dtstart, desc=' after start'))
        self._prtmsg_basic(hms, msg)
        print(str_started_epoch())
        print(str_tostart_epoch())

    def get_desc(self, note=' set'):
        """Get a string describing the state of an instance of the CfgProj"""
        return (
            f'CfgProj {note} {int(exists(self.filename))} '
            f'fname start {self.filename}')

    def read_starttime(self):
        """Get datetime from a starttime file"""
        return self._read_starttime() if exists(self.filename) else None

    def _read_starttime(self):
        with open(self.filename, encoding='utf8') as ifstrm:
            for line in ifstrm:
                line = line.strip()
                # pylint: disable=line-too-long
                assert len(line) == 26, f'len({line})={len(line)}; EXPFMT: 2025-01-22 04:05:00.086891'
                return datetime.strptime(line, FMTDT)
        return None

    def prt_elapsed(self, msg='Timer running'):
        """Print elapsed time if timer is started"""
        # Print elapsed time, if timer was started
        if exists(self.filename):
            dtstart = self._read_starttime()
            hms = self._hms_from_startfile(dtstart)
            return self._prt_elapsed_hms(hms, msg) if hms is not None else str_not_running()
        return None

    def _prt_elapsed_hms(self, hms, msg):
        print(f'{msg}: {hms} H:M:S '
              f"for '{self.project}' ID={self.name}")

    def rm_starttime(self):
        """Remove the starttime file, thus resetting the timer"""
        fstart = self.filename
        if exists(fstart):
            remove(fstart)

    def _hms_from_startfile(self, dtstart):
        """Get the elapsed time starting from time in a starttime file"""
        return datetime.now() - dtstart if dtstart is not None else None


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
