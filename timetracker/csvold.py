"""Local project configuration parser for timetracking"""
# pylint: disable=duplicate-code

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from datetime import timedelta
from datetime import datetime
from logging import debug
from logging import warning
from csv import writer

from timetracker.utils import orange
from timetracker.consts import FMTDT
from timetracker.ntcsv import NTTIMEDATA
from timetracker.csvutils import get_hdr_itr


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
        strptime = datetime.strptime
        with open(self.fcsv, encoding='utf8') as csvstrm:
            hdr, itr = get_hdr_itr(csvstrm)
            self._chk_hdr(hdr)
            for row in itr:
                startdt = strptime(row[2], FMTDT)
                ret.append(nto(
                    start_datetime=startdt,
                    duration=strptime(row[5], FMTDT) - startdt,
                    message=row[7],
                    activity=row[8],
                    tags=row[9]))
        return ret

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
        startdt = datetime.strptime(row[2], FMTDT)
        stopdt  = datetime.strptime(row[5], FMTDT)
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
