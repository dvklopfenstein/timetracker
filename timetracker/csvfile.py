"""Local project configuration parser for timetracking"""
# pylint: disable=duplicate-code

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from datetime import timedelta
from datetime import datetime
from logging import debug
from csv import writer

from timetracker.utils import orange
from timetracker.ntcsv import NTTIMEDATA
from timetracker.csvutils import get_hdr_itr


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
        td_from_str = self.td_from_str
        return sum((td_from_str(row[1]) for row in self.read_all()), start=timedelta())

    def read_all(self):
        """Get all the data in the csv file"""
        with open(self.fcsv, encoding='utf8') as csvstrm:
            hdrs, itr = get_hdr_itr(csvstrm)
            self._chk_hdr(hdrs)
            return list(itr)
        return None

    def wr_stopline(self, dta, dtz, delta, csvfields):
        """Write one data line in the csv file"""
        debug(f'REMOVE THIS ARG dtz({dtz})')
        # Print header into csv, if needed
        if not exists(self.fcsv):
            self._wrhdrs()
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

    def td_from_str(self, txt):
        """Get a timedelta, given a string"""
        slen = len(txt)
        if (slen in {14, 15} and txt[-7] == '.') or slen in {7, 8}:
            return self._td_from_hms(txt, slen)
        daystr, hms = txt.split(',')
        return self._td_from_hms(hms[1:], len(hms)-1) + \
               timedelta(days=int(daystr.split(maxsplit=1)[0]))

    @staticmethod
    def _td_from_hms(txt, slen):
        """Get a timedelta, given 8:00:00 or 12:00:01.100001"""
        if slen in {14, 15} and txt[-7] == '.':
            dto = datetime.strptime(txt, "%H:%M:%S.%f")
            return timedelta(hours=dto.hour,
                             minutes=dto.minute,
                             seconds=dto.second,
                             microseconds=dto.microsecond)
        assert slen in {7, 8}
        dto = datetime.strptime(txt, "%H:%M:%S")
        return timedelta(hours=dto.hour, minutes=dto.minute, seconds=dto.second)

    def _wrhdrs(self):
        with open(self.fcsv, 'w', encoding='utf8') as prt:
            print(','.join(self.hdrs), file=prt)

    def _chk_hdr(self, hdrs):
        """Check the file format"""
        if len(hdrs) != 5:
            print('Expected {len(self.hdrs)} hdrs; got {len(hdrs)}: {hdrs}')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
