#!/usr/bin/env python3
"""Test finding either .timetracker/ proj dir or mount dir"""

from os.path import dirname
from os.path import join
from os.path import ismount
from datetime import timedelta
from timeit import default_timer
from timetracker.cfg.utils import finddirtrk


def test_finddirtrk():
    """Test finding either .timetracker/ proj dir or mount dir"""

    tic = default_timer()
    path = dirname(__file__)
    # Usually '.timetracker'
    trksubdir = '.trkr'

    # Get expected results
    # /cygdrive/c/Users/uname/repos/timetracker/.trkr
    expdir1 = join(dirname(path), trksubdir)
    # /cygdrive/c
    expdir0 = _get_mount_dir(path)

    # Test IN: /cygdrive/c/Users/uname/repos/timetracker/tests/
    # EXP OUT: /cygdrive/c/Users/uname/repos/timetracker/.trkr/
    retdir, found = _run(path, trksubdir)
    assert retdir == expdir1, f'DIR FAILED:\nEXP({expdir1}\nACT:{retdir}'
    assert found

    # Test IN: /cygdrive/c/Users/uname/repos/timetracker/
    # EXP OUT: /cygdrive/c/Users/uname/repos/timetracker/.trkr/
    path = dirname(path)
    retdir, found = _run(path, trksubdir)
    assert retdir == expdir1, f'DIR FAILED:\nEXP({expdir1}\nACT:{retdir}'
    assert found

    # Test IN: /cygdrive/c/Users/uname/repos/
    # EXP OUT: /cygdrive/c/
    path = dirname(path)
    retdir, found = _run(path, trksubdir)
    assert retdir == expdir0, f'DIR FAILED:\nEXP({expdir0}\nACT:{retdir}'
    assert not found

    # Ending message
    print(f'{str(timedelta(seconds=default_timer()-tic))} TEST PASSED')


def _run(path, trksubdir):
    trkdir, found = finddirtrk(path, trksubdir)
    #print(f'START DIR: {path}')
    print(f'TRK DIR: found({int(found)}) {trkdir}')
    return trkdir, found

def _get_mount_dir(path):
    while not ismount(path):
        path = dirname(path)
    return path

if __name__ == '__main__':
    test_finddirtrk()
