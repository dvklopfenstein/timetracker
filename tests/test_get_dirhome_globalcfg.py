#!/usr/bin/env python3
"""Test the stop command"""

from os import environ
from os import unsetenv
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
