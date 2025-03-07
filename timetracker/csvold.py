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
from logging import warning
from csv import reader
from csv import writer

from timetracker.utils import orange
#from timetracker.consts import DIRTRK
from timetracker.consts import FMTDT
from timetracker.consts import FMTDT24HMS
#from timetracker.cfg.utils import get_username
from timetracker.ntcsv import NTTIMEDATA


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

    def get_data(self):
        """Get data where start and stop are datetimes; timdelta is calculated from them"""
        debug('get_data')
        ret = []
        nto = NTTIMEDATA
        with open(self.fcsv, encoding='utf8') as csvstrm:
            _, itr = self._start_readcsv(csvstrm)
            for row in itr:
                startdt = self._getdt(row[2])
                ret.append(nto(
                    start_datetime=startdt,
                    duration=self._getdt(row[5]) - startdt,
                    message=row[7],
                    activity=row[8],
                    tags=row[9]))
        return ret

    def read_totaltime(self):
        """Calculate the total time by parsing the csv"""
        time_total = []
        with open(self.fcsv, encoding='utf8') as csvstrm:
            _, itr = self._start_readcsv(csvstrm)         # hdr (rownum=1)
            self._add_timedelta_from_row(time_total, next(itr), rownum=2)
            for rownum, row in enumerate(itr, 3):
                self._add_timedelta_from_row(time_total, row, rownum)
        return sum(time_total, start=timedelta())

    def wr_stopline(self, dta, dtz, delta, csvfields):
        """Write one data line in the csv file"""
        # Print header into csv, if needed
        if not exists(self.fcsv):
            with open(self.fcsv, 'w', encoding='utf8') as prt:
                print(','.join(self.hdrs), file=prt)
        # Print time information into csv
        with open(self.fcsv, 'a', encoding='utf8') as csvfile:
            data = [dta.strftime("%a"), dta.strftime("%p"), str(dta),
                    dtz.strftime("%a"), dtz.strftime("%p"), str(dtz),
                    str(delta),
                    csvfields.message, csvfields.activity, csvfields.tags]
            writer(csvfile).writerow(data)
            return data
        return None

    def _start_readcsv(self, csvstrm):
        timereader = reader(csvstrm)
        itr = iter(timereader)
        hdr = next(itr)
        self._chk_hdr(hdr)
        return hdr, itr

    def _add_timedelta_from_row(self, time_total, row, rownum):
        startdt = self._getdt(row[2])
        stopdt  = self._getdt(row[5])
        if startdt is None or stopdt is None:
            return
        delta = stopdt - startdt
        if delta.days >= 0:
            time_total.append(delta)
        # https://stackoverflow.com/questions/46803405/python-timedelta-object-with-negative-values
        if delta.days < 0:
            row = ','.join(row)
            warning(f'Warning: Ignoring negative time delta in {self.fcsv}[{rownum}]: {row}')

    @staticmethod
    def _getdt(timestr):
        try:
            return datetime.strptime(timestr, FMTDT)
        except ValueError:
            pass
        try:
            # pylint: disable=fixme
            # TODO: warn to update csv
            return datetime.strptime(timestr, FMTDT24HMS)
        except ValueError as err:
            warning(f'{err}')
            warning(f'UNRECOGNIZED datetime format({timestr})')
            return None

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
