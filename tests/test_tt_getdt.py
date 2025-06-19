#!/usr/bin/env python3
"""Test various methods for converting free text to a timestring"""

from collections import namedtuple
from datetime import timedelta
from csv import writer
from timeit import default_timer
from re import compile as re_compile

from timetracker.epoch.epoch import _get_dt_ampm
from timetracker.epoch.epoch import _conv_timedelta
from timetracker.epoch.epoch import _conv_datetime
from tests.pkgtttest.timestrs import TIMESTRS
from tests.pkgtttest.timestrs import NOW


def test_tt_getdt(fcsv='timetrials_datatime.csv'):
    """Test various methods for converting free text to a timestring"""
    nto = namedtuple('RunTimes', 'DVK DVK_matched dateparser dateparser_matched txt')
    timedata = _run(nto)
    #_prt_timedata(timedata)
    _wr_timedata(fcsv, timedata, nto)


def _run(nto):
    timedata = []
    #cmp_time = re_compile(r'((\d{1,2}):){0,2}(\d{1,2})\s*(?P<AM_PM>[aApP][mM])')
    # pylint: disable=line-too-long
    cmp_time = re_compile(r'((?P<hour>\d{1,2})[^-/_](:(?P<minute>\d{1,2}))?[^-/_](:(?P<second>\d{1,2}))?\s*(?P<AM_PM>[aApP][mM])?)')
    cmp_date = re_compile(r'((?P<year>\d{4})[-/_]?)?(?P<month>\d{1,2})[-/_](?P<day>\d{1,2})')
    print(f'NOW: {NOW}')
    for timestr, expdct in TIMESTRS.items():
        print(f'\nTIMESTR({timestr})')
        tic = default_timer()
        print("SEARCH FOR TIME:", cmp_time.search(timestr))
        print("SEARCH FOR DATE:", cmp_date.search(timestr))
        tt0 = timedelta(seconds=default_timer()-tic)
        print(f'{tt0}    re          ({timestr})')  # {dta}')

        tic = default_timer()
        dta = _get_dt_ampm(timestr, NOW)
        assert dta == expdct['dt'], f'ACT != EXP\nTXT({timestr})\nACT({dta})\nEXP({expdct["dt"]})'
        tta = timedelta(seconds=default_timer()-tic)
        print(f'{tta}    _get_dt_ampm({timestr}) {dta}')

        tic = default_timer()
        dtb = _conv_datetime(timestr, NOW)
        ttb = timedelta(seconds=default_timer()-tic)
        #print(f'{ttb}  _conv_datetime({timestr}) {dtb}')

        tic = default_timer()
        dtc = _conv_timedelta(timestr)
        ttc = timedelta(seconds=default_timer()-tic)
        print(f'{ttc} _conv_timedelta({timestr}) {dtc}')

        faster = ttb.total_seconds()/tta.total_seconds()
        print(f'{faster:10.1f} times faster is trk alg compared to dateparser for "{timestr}"')

        if dta is not None and dtb is not None:
            # dateparser considers a number a month, DVK considers it an hour
            if timestr not in {'12', '13'}:
                assert dta == dtb, f'DVK != DTP\nTXT({timestr})\nDVK({dta})\nDTP({dtb})'

        timedata.append(nto(
            txt=timestr,
            DVK        =tta.total_seconds()*1_000_000,        DVK_matched=dta is not None,
            dateparser =ttb.total_seconds()*1_000_000, dateparser_matched=dtb is not None))

    return timedata

def _prt_timedata(timedata):
    for ntd in timedata:
        print(ntd)

def _wr_timedata(fcsv, timedata, nto):
    with open(fcsv, 'w', encoding='utf-8') as ostrm:
        wrobj = writer(ostrm)
        wrobj.writerow(nto._fields)
        for ntd in timedata:
            wrobj.writerow(ntd)
        print(f'  WROTE: {fcsv}')

if __name__ == '__main__':
    test_tt_getdt()
