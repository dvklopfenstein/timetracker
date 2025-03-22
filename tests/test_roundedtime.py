#!/usr/bin/env python3
"""Test rounding datetime objects"""

from logging import basicConfig
from logging import debug
from logging import DEBUG
from datetime import datetime
from datetime import timedelta

from timetracker.consts import FMTTIME
from timetracker.epoch.calc import RoundTime

from tests.pkgtttest.dts import DT2525
from tests.pkgtttest.dts import get_dt


basicConfig(level=DEBUG)


def test_rounding_now():
    """Test rounding datetime objects"""
    rndobj = RoundTime(15)
    dtobj = datetime.now()
    _run_time_round(rndobj, dtobj)
    _run_time_floor(rndobj, dtobj)
    _run_time_ceil(rndobj, dtobj)

def test_rounding_val():
    """Test rounding datetime objects"""
    rndobj = RoundTime(15)
    dtobj = DT2525
    dtobj = get_dt('2525', hour=16, minute=13, second=25, microsecond=27069)

    results = _run_time_round(rndobj, dtobj)
    _check_results(results, _get_exp_round())

    results = _run_time_floor(rndobj, dtobj)
    _check_results(results, _get_exp_floor())

    results = _run_time_ceil(rndobj, dtobj)
    _check_results(results, _get_exp_ceil())

def _run_time_round(rndobj, dtobj):
    debug('\n\nRUN ROUNDING to 15 MINUTES:')
    results = []
    for idx in range(0, 60, 5):
        dttest = dtobj + timedelta(minutes=idx)
        dtrnd = rndobj.time_round(dttest)
        debug(f' {dttest.strftime(FMTTIME)} -> {dtrnd.strftime(FMTTIME)}')
        results.append((dttest, dtrnd))
    return results

def _run_time_floor(rndobj, dtobj):
    debug('\n\nRUN FLOOR to 15 MINUTES:')
    results = []
    for idx in range(0, 60, 5):
        dttest = dtobj + timedelta(minutes=idx)
        dtfloor = rndobj.time_floor(dttest)
        debug(f' {dttest.strftime(FMTTIME)} -> {dtfloor.strftime(FMTTIME)}')
        assert dttest >= dtfloor
        results.append((dttest, dtfloor))
    return results

def _run_time_ceil(rndobj, dtobj):
    debug('\n\nRUN CEILING to 15 MINUTES:')
    results = []
    for idx in range(0, 60, 5):
        dttest = dtobj + timedelta(minutes=idx)
        dtceiling = rndobj.time_ceil(dttest)
        assert dttest <= dtceiling
        debug(f' {dttest.strftime(FMTTIME)} -> {dtceiling.strftime(FMTTIME)}')
        results.append((dttest, dtceiling))
    return results

def _check_results(results, act2exp):
    for orig, act in results:
        assert act.strftime(FMTTIME) == act2exp[orig.strftime(FMTTIME)]

def _get_exp_round():
    return {
        "16:13:25.027069": "16:15:00.000000",
        "16:18:25.027069": "16:15:00.000000",
        "16:23:25.027069": "16:30:00.000000",
        "16:28:25.027069": "16:30:00.000000",
        "16:33:25.027069": "16:30:00.000000",
        "16:38:25.027069": "16:45:00.000000",
        "16:43:25.027069": "16:45:00.000000",
        "16:48:25.027069": "16:45:00.000000",
        "16:53:25.027069": "17:00:00.000000",
        "16:58:25.027069": "17:00:00.000000",
        "17:03:25.027069": "17:00:00.000000",
        "17:08:25.027069": "17:15:00.000000",
    }

def _get_exp_floor():
    return {
        "16:13:25.027069": "16:00:00.000000",
        "16:18:25.027069": "16:15:00.000000",
        "16:23:25.027069": "16:15:00.000000",
        "16:28:25.027069": "16:15:00.000000",
        "16:33:25.027069": "16:30:00.000000",
        "16:38:25.027069": "16:30:00.000000",
        "16:43:25.027069": "16:30:00.000000",
        "16:48:25.027069": "16:45:00.000000",
        "16:53:25.027069": "16:45:00.000000",
        "16:58:25.027069": "16:45:00.000000",
        "17:03:25.027069": "17:00:00.000000",
        "17:08:25.027069": "17:00:00.000000",
    }

def _get_exp_ceil():
    return {
        "16:13:25.027069": "16:15:00.000000",
        "16:18:25.027069": "16:30:00.000000",
        "16:23:25.027069": "16:30:00.000000",
        "16:28:25.027069": "16:30:00.000000",
        "16:33:25.027069": "16:45:00.000000",
        "16:38:25.027069": "16:45:00.000000",
        "16:43:25.027069": "16:45:00.000000",
        "16:48:25.027069": "17:00:00.000000",
        "16:53:25.027069": "17:00:00.000000",
        "16:58:25.027069": "17:00:00.000000",
        "17:03:25.027069": "17:15:00.000000",
        "17:08:25.027069": "17:15:00.000000",
    }

if __name__ == '__main__':
    test_rounding_now()
    test_rounding_val()
