#!/usr/bin/env python3
"""Test reading and writing csv files using CsvFile"""

from os import system
from os.path import join
from tempfile import TemporaryDirectory
from datetime import datetime
from timetracker.csvfile import CsvFile
from timetracker.ntcsv import get_ntcsv
from timetracker.utils import orange
from timetracker.epoch.calc import td_from_str

def test_csvfile():
    """Test reading and writing csv files using CsvFile"""
    # pylint: disable=too-many-statements
    with TemporaryDirectory() as tmphome:
        fcsv = join(tmphome, 'activities.csv')
        obj = Run(fcsv)
        _pos(obj)
        assert str(obj.obj.read_totaltime_all().results) == "2703168 days, 8:01:06.200003", \
            str(obj.obj.read_totaltime_all())
        _neg(obj)
        assert str(obj.obj.read_totaltime_all().results) == "0:00:00"

        # CSV
        system(f'cat {fcsv}')


def _pos(obj):
    # pylint: disable=too-many-statements
    print(orange("7 chars"))
    #  8:00:00           7
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 17, minute=0, second=0, microsecond=0)
    obj.run(dta, dtz, 'Test a')
    #  0:00:01           7
    dta = datetime(2525, 1, 1, 9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 9, minute=0, second=1, microsecond=0)
    obj.run(dta, dtz, 'Test a')
    #  0:00:01           7
    dta = datetime(2525, 1, 1, 9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 9, minute=1, second=0, microsecond=0)
    obj.run(dta, dtz, 'Test a')
    #  0:00:01           7
    dta = datetime(2525, 1, 1, 9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 9, minute=0, second=0, microsecond=0)
    obj.run(dta, dtz, 'Test a')

    print(orange("8 chars"))
    # 12:00:00           8
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 21, minute=0, second=0, microsecond=0)
    obj.run(dta, dtz, 'Test a')
    # 12:00:01           8
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 21, minute=0, second=1, microsecond=0)
    obj.run(dta, dtz, 'Test a')

    print(orange("14 chars"))
    # 1 day, 0:00:00    14
    dta = datetime(2525, 1, 1,  0, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 2,  0, minute=0, second=0, microsecond=0)
    obj.run(dta, dtz, 'Test a')
    # 1 day, 8:00:00    14
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 2, 17, minute=0, second=0, microsecond=0)
    obj.run(dta, dtz, 'ONE DAY')
    #  0:00:00.000001   14
    dta = datetime(2525, 1, 1, 9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 9, minute=0, second=0, microsecond=1)
    obj.run(dta, dtz, 'Test a')

    print(orange("15 chars"))
    # 1 day, 12:00:00   15
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 2, 21, minute=0, second=0, microsecond=0)
    obj.run(dta, dtz, 'Test a')
    # 12:00:01.100000    15
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 21, minute=0, second=1, microsecond=100000)
    obj.run(dta, dtz, 'Test a')
    # 12:00:01.100001    15
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 21, minute=0, second=1, microsecond=100001)
    obj.run(dta, dtz, 'Test a')
    # 12:00:01.999999    15
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 21, minute=0, second=1, microsecond=999999)
    obj.run(dta, dtz, 'Test a')

    print(orange("Lots of chars"))
    # 2703160 days, 8:00:00.000001   28
    dta = datetime(2525, 1, 2,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(9926, 1, 3, 17, minute=0, second=0, microsecond=1)
    obj.run(dta, dtz, 'Test a')
    # 2703160 days, 8:00:00.000001   28
    dta = datetime(2525, 1, 2,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 3, 17, minute=0, second=0, microsecond=1)
    obj.run(dta, dtz, 'Test a')

def _neg(obj):
    # pylint: disable=too-many-statements
    print(orange("7 chars"))
    #  8:00:00           7
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 17, minute=0, second=0, microsecond=0)
    obj.run(dtz, dta, 'Test a')
    #  0:00:01           7
    dta = datetime(2525, 1, 1, 9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 9, minute=0, second=1, microsecond=0)
    obj.run(dtz, dta, 'Test a')
    #  0:00:01           7
    dta = datetime(2525, 1, 1, 9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 9, minute=1, second=0, microsecond=0)
    obj.run(dtz, dta, 'Test a')
    #  0:00:01           7
    dta = datetime(2525, 1, 1, 9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 9, minute=0, second=0, microsecond=0)
    obj.run(dtz, dta, 'Test a')

    print(orange("8 chars"))
    # 12:00:00           8
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 21, minute=0, second=0, microsecond=0)
    obj.run(dtz, dta, 'Test a')
    # 12:00:01           8
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 21, minute=0, second=1, microsecond=0)
    obj.run(dtz, dta, 'Test a')

    print(orange("14 chars"))
    # 1 day, 0:00:00    14
    dta = datetime(2525, 1, 1,  0, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 2,  0, minute=0, second=0, microsecond=0)
    obj.run(dtz, dta, 'Test a')
    # 1 day, 8:00:00    14
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 2, 17, minute=0, second=0, microsecond=0)
    obj.run(dtz, dta, 'ONE DAY')
    #  0:00:00.000001   14
    dta = datetime(2525, 1, 1, 9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 9, minute=0, second=0, microsecond=1)
    obj.run(dtz, dta, 'Test a')

    print(orange("15 chars"))
    # 1 day, 12:00:00   15
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 2, 21, minute=0, second=0, microsecond=0)
    obj.run(dtz, dta, 'Test a')
    # 12:00:01.100000    15
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 21, minute=0, second=1, microsecond=100000)
    obj.run(dtz, dta, 'Test a')
    # 12:00:01.100001    15
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 21, minute=0, second=1, microsecond=100001)
    obj.run(dtz, dta, 'Test a')
    # 12:00:01.999999    15
    dta = datetime(2525, 1, 1,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 1, 21, minute=0, second=1, microsecond=999999)
    obj.run(dtz, dta, 'Test a')

    print(orange("Lots of chars"))
    # 2703160 days, 8:00:00.000001   28
    dta = datetime(2525, 1, 2,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(9926, 1, 3, 17, minute=0, second=0, microsecond=1)
    obj.run(dtz, dta, 'Test a')
    # 2703160 days, 8:00:00.000001   28
    dta = datetime(2525, 1, 2,  9, minute=0, second=0, microsecond=0)
    dtz = datetime(2525, 1, 3, 17, minute=0, second=0, microsecond=1)
    obj.run(dtz, dta, 'Test a')

# pylint: disable=too-few-public-methods
class Run:
    """Run one test"""

    def __init__(self, fcsv):
        self.fcsv = fcsv
        self.obj = CsvFile(fcsv)

    def run(self, dta, dtz, desc):
        """Write a line into the csv file"""
        ntd = get_ntcsv(desc, 'testing', None)
        data = self.obj.wr_csvline(dta, dtz-dta, ntd)
        tdstr = data[1]
        tdobj = td_from_str(tdstr)
        assert str(tdobj) == tdstr, f'OBJ({tdobj}) != CSVSTR({tdstr})'
        print(f'{len(tdstr):>2} {tdstr:30} {str(tdobj):30} {data[3]}')

def _get_exp():
    return [
        '2525-01-01 09:00:00,8:00:00,Test a,testing,',
    ]

if __name__ == '__main__':
    test_csvfile()
