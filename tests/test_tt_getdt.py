#!/usr/bin/env python3
"""Test various methods for converting free text to a timestring"""

from collections import namedtuple
from datetime import timedelta
from datetime import datetime
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
    # pylint: disable=too-many-locals
    timedata = []
    #cmp_time = re_compile(r'((\d{1,2}):){0,2}(\d{1,2})\s*(?P<AM_PM>[aApP][mM])')
    reobj = _ReDatetime()
    print(f'NOW: {NOW}')
    for timestr, expdct in TIMESTRS.items():
        # pylint: disable=too-many-locals
        print(f'\nTIMESTR({timestr})')
        tic = default_timer()
        dtre = reobj.search(timestr)
        tt0 = timedelta(seconds=default_timer()-tic)
        print(f'{tt0}    re          ({timestr}) {dtre}')

        tic = default_timer()
        dta = _get_dt_ampm(timestr, NOW)
        assert dta == expdct['dt'], f'ACT != EXP\nTXT({timestr})\nACT({dta})\nEXP({expdct["dt"]})'
        #assert dta == dtre, f'RE != ME\nTXT({timestr})\nRE({dtre})\nME({dta})'
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


class _ReDatetime:
    """Compare custom solution to Python re solution"""
    # pylint: disable=too-few-public-methods

    # pylint: disable=line-too-long
    cmp_time = re_compile(r'((?<![-\d/])(?P<hour>\d{1,2})(?![-\d/])(:(?P<minute>\d{1,2}))?(:(?P<second>\d{1,2}))?\s*(?P<AM_PM>[aApP][mM])?)')
    cmp_date = re_compile(r'((?P<year>\d{4})[-/_]?)?(?P<month>\d{1,2})[-/_](?P<day>\d{1,2})')

    def search(self, timestr):
        """Use Python `re` to search for date and time"""
        mtch_time = self._search_time(timestr)
        mtch_date = self._search_date(timestr)
        print("SEARCH FOR TIME:", mtch_time, mtch_time.groupdict() if mtch_time else '')
        print("SEARCH FOR DATE:", mtch_date, mtch_date.groupdict() if mtch_date else '')
        if mtch_time is None or mtch_time.group('hour') is None:
            return None
        dct_hms = self._get_hms(mtch_time)
        dct_ymd = self._get_ymd(mtch_date)
        dct = {**dct_ymd, **dct_hms}
        if (m := mtch_time.group('AM_PM')) is not None:
            if not self._ampm(dct, m):
                return None
        print("SEARCH DATETIME:", dct)
        if dct:
            try:
                ret = datetime(year=dct['year'], month=dct['month'], day=dct['day'],
                               hour=dct['hour'],
                               minute=dct['minute'],
                               second=dct['second'])
            except ValueError:
                print(f'BAD datetime INPUT: {dct}')
            else:
                return ret
        return None

    def _get_hms(self, mtch):
        return {'hour':  int(mtch.group('hour')),
                'minute': int(m) if (m := mtch.group('minute'))   else 0,
                'second':   int(m) if (m := mtch.group('second')) else 0}


    def _ampm(self, dct, ampm):
        if ampm is None:
            return True
        ampm = ampm.upper()
        if ampm == 'PM':
            if 0 <= (hour := dct['hour']) < 12:
                dct['hour'] = hour + 12
            elif hour != 12:
                return False
        else:
            assert ampm == 'AM', dct
            if dct['hour'] == 12:
                dct['hour'] = 0
        return True

    def _get_ymd(self, mtch):
        if mtch:
            return {'year':  int(m) if (m := mtch.group('year'))  else NOW.year,
                    'month': int(m) if (m := mtch.group('month')) else NOW.month,
                    'day':   int(m) if (m := mtch.group('day'))   else NOW.day}
        return {'year':  NOW.year,
                'month': NOW.month,
                'day':   NOW.day}

    def _search_time(self, timestr):
        """Use Python re to search for time"""
        return self.cmp_time.search(timestr)

    def _search_date(self, timestr):
        """Use Python re to search for time"""
        return self.cmp_date.search(timestr)

if __name__ == '__main__':
    test_tt_getdt()
