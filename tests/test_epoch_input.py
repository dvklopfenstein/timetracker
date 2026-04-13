#!/usr/bin/env python3
"""Test processing a researcher datetime or elapsed time string"""

from logging import basicConfig
from logging import DEBUG
from logging import debug
from datetime import datetime
from datetime import timedelta

# tempora parse_timedelta: 30:00 -> 1 day, 6:00:00, not 30 minutes
# from tempora import parse_timedelta
from pytimeparse2 import parse as parse_tdelta
from dateutil.parser import parse as parse_dt

from timetracker.consts import FMTDT_H
from timetracker.epoch.calc import RoundTime
from tests.pkgtttest.dts import DT2525

basicConfig(level=DEBUG)


def test_epoch_input():
    """Test processing a researcher datetime or elapsed time string"""

    print('\nTEST TIME DELTAs:')
    for txt, exp in _get_tdelta_n_exp():
        act = parse_tdelta(txt)
        debug(f'{txt:20} {act}')
        assert isinstance(act, int)
        assert act == exp, f'TDELTA({txt}): ACT({act}) != EXP({exp})'

    print('\nTEST DATES:')
    today = datetime.today()
    dttest = datetime.strptime(f"Wed {today.year}-02-19 03:00:51 PM", FMTDT_H)
    for idx, (txt, exp) in enumerate(_get_dt_n_expdt(dttest, today)):
        act = parse_dt(txt)
        debug(f' TXTSTR: {txt:26} ACT: {str(act):26} EXP: {exp}')
        if act != exp:
            print(f'\n{idx}) ACT != EXP:\n TSTR({txt})\nACT({act})\nEXP({exp})')
        #assert act == exp, f'{idx}) ACT != EXP:\n TSTR({txt})\nACT({act})\nEXP({exp})'
        #assert isinstance(act, int)

    # "Today" is 2525
    print('\nTEST DATE 2525:')
    assert str(parse_dt('4am',           default=DT2525)) == "2525-01-01 04:00:00"
    assert str(parse_dt('5:00 pm',       default=DT2525)) == "2525-01-01 17:00:00"
    assert str(parse_dt('5:30pm',        default=DT2525)) == "2525-01-01 17:30:00"
    assert str(parse_dt('2-19 5:30 pm',  default=DT2525)) == "2525-02-19 17:30:00"
    debug('TEST PASSED')


def _get_tdelta_n_exp():
    """Get tests and the expected result"""
    min30 = 30*60    # Seconds in 30 minuts
    hour4 = 4*60*60  # Seconds in  4 hours
    return (
        ("30 minutes", min30),
        ("30 min",     min30),
        ("30min",      min30),
        ("00:30:00",   min30),
        ("30:00",      min30),
        ("4 hours",    hour4),
        ("04:00:00",   hour4),
        ("4:00:00",    hour4),
    )

def _get_dt_n_expdt(dtval, today):
    """Get tests and the expected result"""
    # Round to not worry about delta time executed in test
    round30min = RoundTime(30)
    dtrnddn = round30min.time_ceil(dtval + timedelta(minutes=90))
    dtrndup = round30min.time_ceil(dtval + timedelta(minutes=120))
    year = today.year
    #    text-string                  expected
    return (
        (f"{year}-02-19 17:00:00",    dtrnddn ),
        (f"{year}-02-19 05:00:00 pm", dtrnddn ),
        ("02-19 17:00:00",            dtrnddn ),
        ("02-19 05:00:00 pm",         dtrnddn ),
        ("02-19 5pm",                 dtrnddn ),
        ("02-19 5:00 pm",             dtrnddn ),
        ("2-19 5:30 pm",              dtrndup),
        # pylint: disable=line-too-long
        ("5:00 pm", datetime(year, today.month, today.day, dtrnddn.hour, dtrnddn.minute, dtrnddn.second)),
        ("5:30 pm", datetime(year, today.month, today.day, dtrndup.hour, dtrndup.minute, dtrndup.second)),
        # ("4 days, 9:33:54.912101", dtrnddn),  # No
    )


if __name__ == '__main__':
    test_epoch_input()
