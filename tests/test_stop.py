#!/usr/bin/env python3
"""Test the stop command"""

#from os import makedirs
#from os.path import exists
#from os.path import join
#from logging import basicConfig
#from logging import DEBUG
#from tempfile import TemporaryDirectory
#from tests.pkgtttest.mkprojs import mkdirs
#from tests.pkgtttest.mkprojs import findhome
#from subprocess import run
from collections import namedtuple
from pytest import raises
from timetracker.cmd.stop import _run_stop


#basicConfig(level=DEBUG)

SEP1 = f'\n{"="*80}\n'
NTO = namedtuple("CsvFields", "message activity tags")

def test_stop():
    """Test the stop command"""
    filename_config = 'tmpconfig'
    csvfields = NTO(message='Testing writing csv',
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
