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
from timetracker.cmd.stop import run_stop


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
    run_stop(filename_config, csvfields, quiet=quiet, keepstart=keepstart)

if __name__ == '__main__':
    test_stop()
