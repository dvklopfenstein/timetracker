"""Local project configuration parser for timetracking"""
# pylint: disable=duplicate-code

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from collections import namedtuple
from datetime import timedelta
from logging import debug
from logging import warning
from csv import writer

from timetracker.utils import orange
from timetracker.csvutils import get_hdr_itr
from timetracker.epoch.calc import dt_from_str


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

    def get_ntdata(self):
        """Get data where start and stop are datetimes; timdelta is calculated from them"""
        debug('get_ntdata')
        ret = []
        nto = namedtuple('TimeDataOrig', 'start_datetime duration activity message tags')
        with open(self.fcsv, encoding='utf8') as csvstrm:
            hdr, itr = get_hdr_itr(csvstrm)
            self._chk_hdr(hdr)
            for idx, row in enumerate(itr, 2):
                assert len(row) == 10, self._errmsg(row, idx)
                startdt = dt_from_str(row[2])
                ret.append(nto(
                    start_datetime=startdt,
                    duration=dt_from_str(row[5]) - startdt,
                    message=row[7],
                    activity=row[8],
                    tags=row[9]))
        return ret

    def _errmsg(self, row, idx):
        ret = [
            f'EXPECTED 10 COLUMNS, GOT {len(row)}',
            f'LINE {idx} FILE {self.fcsv}',
            '    HEADERS        VALUE',
        ]
        for cnum, (elem, hdr) in enumerate(zip(row, self.hdrs)):
            ret.append(f'{cnum:2}) {hdr:14} {elem}')
        return '\n'.join(ret)

    def read_totaltime(self):
        """Calculate the total time by parsing the csv"""
        time_total = []
        with open(self.fcsv, encoding='utf8') as csvstrm:
            hdr, itr = get_hdr_itr(csvstrm)         # hdr (rownum=1)
            self._chk_hdr(hdr)
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
            writer(csvfile, lineterminator='\n').writerow(data)
            return data
        return None

    def _add_timedelta_from_row(self, time_total, row, rownum):
        startdt = dt_from_str(row[2])
        stopdt  = dt_from_str(row[5])
        if startdt is None or stopdt is None:
            return
        delta = stopdt - startdt
        if delta.days >= 0:
            time_total.append(delta)
        # https://stackoverflow.com/questions/46803405/python-timedelta-object-with-negative-values
        if delta.days < 0:
            row = ','.join(row)
            warning(f'Warning: Ignoring negative time delta in {self.fcsv}[{rownum}]: {row}')

    def _chk_hdr(self, hdrs):
        """Check the file format"""
        if len(hdrs) != 10:
            print('Expected {len(self.hdrs)} hdrs; got {len(hdrs)}: {hdrs}')
        if hdrs[2] != 'start_datetime' or hdrs[5] != 'stop_datetime':
            print('Unexpected start and stop datetimes: {self.fcsv}')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
