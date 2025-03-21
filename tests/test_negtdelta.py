#!/usr/bin/env python3
"""Test processing a researcher datetime or elapsed time string"""

from logging import basicConfig
from logging import DEBUG
#from logging import debug
# datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)
# timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
from datetime import timedelta

from timetracker.epoch.calc import str_td
from tests.pkgtttest.dts import DT2525
from tests.pkgtttest.dts import get_dt

basicConfig(level=DEBUG)


def test_epoch_input():
    """Test processing negative timedeltas"""
    # https://docs.python.org/3/library/datetime.html#datetime.timedelta
    tdelta = _get_tdelta(hours=-14)
    # -1 day, 10:00:00 == -14:00:00
    print(f'timedelta+0: {tdelta + timedelta()}')
    print(f'timedelta: {tdelta}')
    print(f'totalsecs: {tdelta.total_seconds()}')
    print(f'14*3600:    {14*3600}')
    print(str_td(tdelta))


    tdeltas = [timedelta(seconds=1), timedelta(seconds=3), timedelta(seconds=5)]
    s = timedelta()
    cumsum = [(s:=s+i) for i in tdeltas]
    print(tdeltas)
    print(cumsum)

def _get_tdelta(hours):
    if hours < 0:
        return DT2525 - get_dt('2525', -1*hours, 0, 0, 0)
    return get_dt('2525', hours, 0, 0, 0) > DT2525



if __name__ == '__main__':
    test_epoch_input()
