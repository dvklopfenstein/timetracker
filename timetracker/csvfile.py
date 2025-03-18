"""Local project configuration parser for timetracking"""
# pylint: disable=duplicate-code

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from datetime import timedelta
from logging import debug
from csv import writer

from timetracker.utils import orange
from timetracker.ntcsv import NTTIMEDATA
from timetracker.csvutils import get_hdr_itr
from timetracker.csvutils import td_from_str


class CsvFile:
    """Manage CSV file"""

    hdrs = [
        'start_datetime', # 0
        'duration',       # 1
        'activity',       # 2
        'message',        # 3
        'tags',           # 4
    ]

    def __init__(self, csvfilename):
        self.fcsv = csvfilename
        debug(orange(f'Starttime args {int(exists(self.fcsv))} self.fcsv {self.fcsv}'))

    def get_data(self):
        """Get data where start and stop are datetimes; timdelta is calculated from them"""
        debug('get_data')
        nto = NTTIMEDATA
        with open(self.fcsv, encoding='utf8') as csvstrm:
            hdrs, itr = get_hdr_itr(csvstrm)
            self._chk_hdr(hdrs)
            return [nto._make(*row) for row in itr]
        return None

    def read_totaltime_all(self):
        """Calculate the total time by parsing the csv"""
        return sum((td_from_str(row[1]) for row in self.read_all()), start=timedelta())

    def read_all(self):
        """Get all the data in the csv file"""
        with open(self.fcsv, encoding='utf8') as csvstrm:
            hdrs, itr = get_hdr_itr(csvstrm)
            self._chk_hdr(hdrs)
            return list(itr)
        return None

    def wr_stopline(self, dta, delta, csvfields):
        """Write one data line in the csv file"""
        # Print header into csv, if needed
        if not exists(self.fcsv):
            self.wr_hdrs()
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

    def wr_hdrs(self):
        """Write header"""
        with open(self.fcsv, 'w', encoding='utf8') as prt:
            print(','.join(self.hdrs), file=prt)

    def _chk_hdr(self, hdrs):
        """Check the file format"""
        if len(hdrs) != 5:
            print('Expected {len(self.hdrs)} hdrs; got {len(hdrs)}: {hdrs}')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
