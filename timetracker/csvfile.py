"""Local project configuration parser for timetracking"""
# pylint: disable=duplicate-code

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from collections import namedtuple
from datetime import timedelta
from logging import debug
# https://docs.python.org/3/library/csv.html
from csv import writer

from timetracker.utils import orange
from timetracker.csvutils import get_hdr_itr
from timetracker.epoch.calc import dt_from_str
from timetracker.epoch.calc import td_from_str


class CsvFile:
    """Manage CSV file"""

    hdrs = [
        'start_datetime', # 0
        'duration',       # 1
        'activity',       # 2
        'message',        # 3
        'tags',           # 4
    ]

    nto = namedtuple('TimeData', hdrs)
    ntrdcsv = namedtuple('RdCsv', 'results error')

    def __init__(self, csvfilename):
        self.fcsv = csvfilename
        debug(orange(f'Starttime args {int(exists(self.fcsv))} self.fcsv {self.fcsv}'))

    def get_ntdata(self):
        """Get data where start and stop are datetimes; timdelta is calculated from them"""
        return self._read_csv(self._get_ntdata)

    def read_totaltime_all(self):
        """Calculate the total time by parsing the csv"""
        return self._read_csv(self._sum_time)

    def wr_stopline(self, dta, delta, csvfields):
        """Write one data line in the csv file"""
        # Print header into csv, if needed
        if not exists(self.fcsv):
            with open(self.fcsv, 'w', encoding='utf8') as csvfile:
                self.wr_hdrs(csvfile)
        # Print time information into csv
        with open(self.fcsv, 'a', encoding='utf8') as csvfile:
            # timedelta(days=0, seconds=0, microseconds=0,
            #           milliseconds=0, minutes=0, hours=0, weeks=0)
            # Only days, seconds and microseconds are stored internally.
            # Arguments are converted to those units:
            data = [str(dta),
                    str(delta),
                    csvfields.activity, csvfields.message, csvfields.tags]
            writer(csvfile, lineterminator='\n').writerow(data)
            return data
        return None

    def wr_hdrs(self, prt):
        """Write header"""
        print(','.join(self.hdrs), file=prt)

    # ------------------------------------------------------------------
    def _get_ntdata(self, csvlines):
        """Get data where start and stop are datetimes; timdelta is calculated from them"""
        debug('get_ntdata')
        nto = self.nto
        def _get_nt(row):
            return nto(
                start_datetime=dt_from_str(row[0]),
                duration=td_from_str(row[1]),
                activity=row[2],
                message=row[3],
                tags=row[4])
        return [_get_nt(row) for row in csvlines]

    @staticmethod
    def _sum_time(csvlines):
        return sum((td_from_str(row[1]) for row in csvlines), start=timedelta())

    def _chk_hdr(self, hdrs):
        """Check the file format"""
        if len(hdrs) != 5:
            print('Expected {len(self.hdrs)} hdrs; got {len(hdrs)}: {hdrs}')

    def _read_csv(self, fnc_csvlines):
        """Read a global or project config file only if it exists and is readable"""
        error = None
        try:
            fptr = open(self.fcsv, encoding='utf8')
        except (FileNotFoundError, PermissionError, OSError) as err:
            error = err
            #fnc_err(f'Note: {err.args[1]}: {self.fcsv}')
            ##fnc_err(err)
            #print(f'{type(err).__name__}{err.args}')
        else:
            with fptr as csvstrm:
                hdrs, itr = get_hdr_itr(csvstrm)
                self._chk_hdr(hdrs)
                return self.ntrdcsv(results=fnc_csvlines(itr), error=error)
        return self.ntrdcsv(results=None, error=error)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
