#!/usr/bin/env python
"""Test speed savings from lazy import"""

from timeit import default_timer
from datetime import timedelta


def test_tt_fncs(num_p_batch=1):
    """Test speed savings from lazy import"""
    # pylint: disable=import-outside-toplevel
    mintime_slow = timedelta(seconds=1000)
    for _ in range(num_p_batch):
        tic = default_timer()
        import tests.pkgtttest.fncs
        del tests
        mintime_slow = min(mintime_slow, timedelta(seconds=default_timer()-tic))
    print(mintime_slow)

    mintime_fast = timedelta(seconds=1000)
    for _ in range(num_p_batch):
        tic = default_timer()
        import timetracker.cmd.fncs
        del timetracker
        mintime_fast = min(mintime_fast, timedelta(seconds=default_timer()-tic))
    print(mintime_fast)

    assert mintime_fast < mintime_slow

    faster = mintime_slow.total_seconds()/mintime_fast.total_seconds()
    print(f'{faster:10.1f} times faster is import fncs compared to regular import')


def test_tt_ospath(num_p_batch=1):
    """Test speed savings from lazy import"""
    # pylint: disable=import-outside-toplevel,too-many-locals
    mintime_slow = timedelta(seconds=1000)
    for _ in range(num_p_batch):
        tic = default_timer()
        from os.path import exists
        from os.path import relpath
        from os.path import abspath
        from os.path import dirname
        from os.path import join
        from os.path import ismount
        from os.path import basename
        from os.path import normpath
        from os.path import realpath
        from logging import debug
        from timetracker.consts import DIRTRK
        del exists
        del relpath
        del abspath
        del dirname
        del join
        del ismount
        del basename
        del normpath
        del realpath
        del debug
        del DIRTRK
        mintime_slow = min(mintime_slow, timedelta(seconds=default_timer()-tic))
    print(mintime_slow)

    mintime_fast = timedelta(seconds=1000)
    for _ in range(num_p_batch):
        tic = default_timer()
        import os.path as os_path
        del os_path
        mintime_fast = min(mintime_fast, timedelta(seconds=default_timer()-tic))
    print(mintime_fast)

    assert mintime_fast < mintime_slow

    faster = mintime_slow.total_seconds()/mintime_fast.total_seconds()
    print(f'{faster:10.1f} times faster is import fncs compared to regular import')


if __name__ == '__main__':
    test_tt_fncs()
    test_tt_ospath()
