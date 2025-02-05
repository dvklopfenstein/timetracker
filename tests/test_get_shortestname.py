#!/usr/bin/env python3
"""Test the stop command"""

#from os import makedirs
#from os.path import exists
#from os.path import join
from logging import basicConfig
#from logging import DEBUG
from logging import debug
#from tempfile import TemporaryDirectory
#from tests.pkgtttest.mkprojs import mkdirs
#from tests.pkgtttest.mkprojs import findhome
#from subprocess import run
#from collections import namedtuple
#from timetracker.cfg.utils import get_shortest_name


#basicConfig(level=DEBUG)
basicConfig()

SEP = f'\n{"="*80}\n'

def test_get_shortestname():
    """Test the get_shortest_name function"""
    debug(f'{SEP}RUNNING TEST')
    print('TEST PASSED')

if __name__ == '__main__':
    test_get_shortestname()
