"""Local project configuration parser for timetracking"""
# pylint: disable=duplicate-code

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

#from os import remove
from os.path import exists
#from os.path import basename
#from os.path import join
#from os.path import abspath
#from os.path import dirname
#from os.path import normpath
from datetime import timedelta
from datetime import datetime
from logging import debug
from csv import reader

from timetracker.utils import orange
#from timetracker.consts import DIRTRK
from timetracker.consts import FMTDT
#from timetracker.cfg.utils import get_username


class CsvFile:
    """Manage CSV file"""

    hdrs = [
        'start_day',
        'xm',
        'start_datetime',
        # Stop
        'stop_day',
        'zm',
        'stop_datetime',
        # Duration
        'duration',
        # Info
        'message',
        'activity',
        'tags',
    ]

    def __init__(self, csvfilename):
        self.fcsv = csvfilename
        debug(orange(f'Starttime args {int(exists(self.fcsv))} self.fcsv {self.fcsv}'))

    def read_totaltime(self):
        """Read the csv"""
        time_total = []
        with open(self.fcsv, encoding='utf8') as csvstrm:
            timereader = reader(csvstrm)
            itr = iter(timereader)
            hdr = next(itr)
            self._chk_hdr(hdr)
            self._add_timedelta_from_row(time_total, next(itr), 2)
            for rnum, row in enumerate(itr, 3):
                self._add_timedelta_from_row(time_total, row, rnum)
        return sum(time_total, start=timedelta())

    def _add_timedelta_from_row(self, time_total, row, rnum):
        delta = datetime.strptime(row[5], FMTDT) - datetime.strptime(row[2], FMTDT)
        if delta.days >= 0:
            time_total.append(delta)
        # https://stackoverflow.com/questions/46803405/python-timedelta-object-with-negative-values
        if delta.days < 0:
            row = ','.join(row)
            print(f'Warning: Ignoring negative time delta in {self.fcsv}[{rnum}]: {row}')

    def _chk_hdr(self, hdrs):
        """Check the file format"""
        if len(self.hdrs) != 10:
            print('Expected {len(self.hdrs)} hdrs; got {len(hdrs)}: {hdrs}')
        if hdrs[2] != 'start_datetime' or hdrs[5] != 'stop_datetime':
            print('Unexpected start and stop datetimes: {self.fcsv}')

    def check(self):
        """Check that csv lines are valid and correct"""
        with open(self.fcsv, encoding='utf8') as csvstrm:
            timereader = reader(csvstrm)
            itr = iter(timereader)
            hdr = next(itr)
            self._chk_hdr(hdr)
            #self._add_timedelta_from_row(time_total, next(itr), 2)
            for rnum, row in enumerate(itr, 3):
                # pylint: disable=fixme
                # TODO
                assert rnum
                assert row


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
