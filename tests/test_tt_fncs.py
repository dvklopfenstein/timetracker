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

    _chk(mintime_slow, mintime_fast, 'import-all-fncs', 'import-one-fnc')


def test_tt_ospath_a(num_p_batch=1000):
    """Test speed savings from lazy import"""
    # pylint: disable=import-outside-toplevel
    mintime_slow = _mintime_os_pathn(num_p_batch)
    mintime_fast = _mintime_os_path1(num_p_batch)
    _chk(mintime_slow, mintime_fast, 'os.path', 'os_path')

def test_tt_ospath_b(num_p_batch=1000):
    """Test speed savings from lazy import"""
    # pylint: disable=import-outside-toplevel
    mintime_slow = _mintime_os_pathn(num_p_batch)
    mintime_fastb = _mintime_os_path1b(num_p_batch)
    _chk(mintime_slow, mintime_fastb, 'os.path', 'os_path + fncs')



def _chk(mintime_slow, mintime_fast, slow_desc, fast_desc):
    if mintime_fast > mintime_slow:
        print(f'FAST[{fast_desc}]({mintime_fast}) NOT < '
              f'SLOW[{slow_desc}]({mintime_slow})')

    if (min_secs := mintime_fast.total_seconds()) != 0:
        faster = mintime_slow.total_seconds()/min_secs
        print(f'{faster:10.1f} times faster is import {fast_desc} '
              f'compared to import {slow_desc}')


def _mintime_os_path1(num_p_batch):
    mintime_fast = timedelta(seconds=1000)
    for _ in range(num_p_batch):
        tic = default_timer()
        # pylint: disable=import-outside-toplevel
        import os.path as os_path
        mintime_fast = min(mintime_fast, timedelta(seconds=default_timer()-tic))
        del os_path
    print(mintime_fast)
    return mintime_fast

def _mintime_os_path1b(num_p_batch):
    mintime_fast = timedelta(seconds=1000)
    for _ in range(num_p_batch):
        tic = default_timer()
        # pylint: disable=import-outside-toplevel
        import os.path as os_path
        # pylint: disable=pointless-statement
        os_path.exists
        os_path.relpath
        os_path.abspath
        os_path.dirname
        os_path.join
        os_path.ismount
        os_path.basename
        os_path.normpath
        os_path.realpath
        mintime_fast = min(mintime_fast, timedelta(seconds=default_timer()-tic))
        del os_path
    print(mintime_fast)
    return mintime_fast

def _mintime_os_pathn(num_p_batch):
    mintime_slow = timedelta(seconds=1000)
    for _ in range(num_p_batch):
        tic = default_timer()
        # pylint: disable=import-outside-toplevel
        from os.path import exists
        from os.path import relpath
        from os.path import abspath
        from os.path import dirname
        from os.path import join
        from os.path import ismount
        from os.path import basename
        from os.path import normpath
        from os.path import realpath
        mintime_slow = min(mintime_slow, timedelta(seconds=default_timer()-tic))
        del exists
        del relpath
        del abspath
        del dirname
        del join
        del ismount
        del basename
        del normpath
        del realpath
    print(mintime_slow)
    return mintime_slow

if __name__ == '__main__':
    test_tt_fncs()
    test_tt_ospath_a()
    test_tt_ospath_b()
