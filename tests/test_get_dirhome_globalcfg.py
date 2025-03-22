#!/usr/bin/env python3
"""Test the stop command"""

from os import environ
from os import unsetenv
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
from timetracker.cmd.stop import run_stop
from timetracker.cfg.utils import get_filename_globalcfg


#basicConfig(level=DEBUG)

def test_get_filename_globalcfg():
    """Test the get_filename_globalcfg function"""
    print(get_filename_globalcfg())
    # Unset the environment variable **only** for this test
    unsetenv('TIMETRACKERCONF')
    assert 'TIMETRACKERCONF' not in environ
    #print(environ['TIMETRACKERCONF'])


if __name__ == '__main__':
    test_get_filename_globalcfg()
