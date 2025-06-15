#!/usr/bin/env python3
"""Test various methods for converting free text to a timestring"""

from datetime import timedelta
from timeit import default_timer
from timetracker.epoch.epoch import _get_dt_ampm
from timetracker.epoch.epoch import _conv_timedelta
from timetracker.epoch.epoch import _conv_datetime
from tests.pkgtttest.timestrs import TIMESTRS
from tests.pkgtttest.timestrs import NOW


def test_tt_getdt():
    """Test various methods for converting free text to a timestring"""
    print(f'NOW: {NOW}')
    for timestr, expdct in TIMESTRS.items():
        print(f'\nTIMESTR({timestr})')

        tic = default_timer()
        dta = _get_dt_ampm(timestr, NOW)
        assert dta == expdct['dt']
        tta = timedelta(seconds=default_timer()-tic)
        print(f'{tta}    _get_dt_ampm({timestr}) {dta}')

        tic = default_timer()
        dtb = _conv_datetime(timestr, NOW)
        ttb = timedelta(seconds=default_timer()-tic)
        print(f'{ttb}  _conv_datetime({timestr}) {dtb}')

        tic = default_timer()
        dtc = _conv_timedelta(timestr)
        ttc = timedelta(seconds=default_timer()-tic)
        print(f'{ttc} _conv_timedelta({timestr}) {dtc}')

        if dta is not None and dtb is not None:
            assert dta == dtb


if __name__ == '__main__':
    test_tt_getdt()
