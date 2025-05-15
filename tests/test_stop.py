#!/usr/bin/env python3
"""Test the stop command"""

from pytest import raises
from timetracker.ntcsv import NTCSV
from timetracker.cmd.stop import _run_stop


def test_stop():
    """Test the stop command"""
    filename_config = 'tmpconfig'
    csvfields = NTCSV(message='Testing writing csv',
                      activity='',
                      tags='')
    quiet = False
    keepstart = False
    # 0 0
    # 0 1
    # 1 0
    # 1 1
    #try:
    #    _run_stop(filename_config, csvfields, quiet=quiet, keepstart=keepstart)
    #except SystemExit as err:
    #    print(err)
    #print('TEST PASSED')
    with raises(SystemExit) as excinfo:
        _run_stop(filename_config, 'USER', csvfields, quiet=quiet, keepstart=keepstart)
    assert excinfo.value.code == 0
    print('TEST PASSED')


if __name__ == '__main__':
    test_stop()
