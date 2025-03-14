#!/usr/bin/env python3
"""Various tests when the project config file does not exist"""

from os import system
from os.path import join
from logging import basicConfig
#from logging import DEBUG
from tempfile import TemporaryDirectory
from timetracker.consts import FILENAME_GLOBALCFG
from timetracker.cfg.finder import CfgFinder
from timetracker.cmd.init import run_init_test
from timetracker.cmd.start import run_start
from timetracker.cmd.stop import run_stop
from timetracker.ntcsv import get_ntcsv
from tests.pkgtttest.dts import DTBEGIN
from tests.pkgtttest.mkprojs import findhome_str
from tests.pkgtttest.mkprojs import mkdirs


basicConfig()
#basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'

def test_get_filename_csv():
    """Test getting a csv name when the project config file does not exist"""
    with TemporaryDirectory() as tmphome:
        dircsv = None
        now = DTBEGIN
        username = 'shopper'
        # /tmp/tmp8ccq7y_9/proj/apples
        # /tmp/tmp8ccq7y_9/proj/blueberries
        # /tmp/tmp8ccq7y_9/proj/cacao
        projname2projdir = mkdirs(tmphome)
        print(findhome_str(tmphome))
        for projname, projdir in projname2projdir.items():
            finder = CfgFinder(projdir)
            cfgfilename = finder.get_cfgfilename()
            fcfgg = join(tmphome, FILENAME_GLOBALCFG)
            run_init_test(cfgfilename, dircsv, projname, fcfgg)
            for idx in range(2, 12, 2):
                run_start(cfgfilename, username, defaultdt=now, start_at=f'{idx}pm')
                ntcsv = get_ntcsv(f'{projname} {username} {idx}')
                run_stop(cfgfilename, username, ntcsv, defaultdt=now, stop_at=f'{idx+1}pm')
            print(f'{projname:11} {projdir} {cfgfilename}')
            system(f'cat {cfgfilename}')
        print(findhome_str(tmphome))


if __name__ == '__main__':
    test_get_filename_csv()
