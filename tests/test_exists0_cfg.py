#!/usr/bin/env python3
"""Various tests when the project config file does not exist"""

#from os import makedirs
#from os.path import exists
#from os.path import join
from logging import basicConfig
#from logging import DEBUG
#from logging import debug
from tempfile import TemporaryDirectory
#from tests.pkgtttest.mkprojs import mkdirs
#from tests.pkgtttest.mkprojs import findhome
#from subprocess import run
#from collections import namedtuple
#from timetracker.cfg.utils import get_shortest_name
from timetracker.cfg.cfg_local  import CfgProj
from tests.pkgtttest.runfncs import proj_setup


#basicConfig(level=DEBUG)
basicConfig()

SEP = f'\n{"="*80}\n'

def test_get_filename_csv(project='apples', dircur='dirproj', username='piemaker'):
    """Test getting a csv name when the project config file does not exist"""
    with TemporaryDirectory() as tmphome:
        cfgname, finder, exp = proj_setup(tmphome, project, dircur, dirgit01=True)
        cfgproj = CfgProj(cfgname, dirhome=tmphome)
        fcsv = cfgproj.get_filename_csv(username)
        assert fcsv is None, f'SHOULD BE NONE WHEN PROJ CFG NOT EXIST; fcsv({fcsv})'


if __name__ == '__main__':
    test_get_filename_csv()
