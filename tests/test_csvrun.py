#!/usr/bin/env python3
"""Test `trk stop --at`"""

from os import system
from os.path import exists
from os.path import join
#from logging import basicConfig
#from logging import DEBUG
from datetime import timedelta
from tempfile import TemporaryDirectory
from timetracker.consts import FILENAME_GLOBALCFG
from timetracker.utils import yellow
from timetracker.ntcsv import get_ntcsv
from timetracker.cmd.init import run_init_test
from timetracker.cmd.start import run_start
from timetracker.cmd.stop import run_stop
from tests.pkgtttest.dts import get_dt
from tests.pkgtttest.runfncs import proj_setup


def test_stopat(project='pumpkin', username='carver', dircsv=None):
    """Test rewriting csv file"""
    #basicConfig(level=DEBUG)

    with TemporaryDirectory() as tmphome:
        cfgname, _, _ = proj_setup(tmphome, project, dircur='dirproj', dirgit01=True)
        fcfgg = join(tmphome, FILENAME_GLOBALCFG)
        cfgp, _ = run_init_test(cfgname, dircsv, project, fcfgg, quiet=False)  # cfgg
        assert cfgname == cfgp.filename, f'{cfgname} != {cfgp.filename}'

        # Write in old format
        dta = get_dt(yearstr='2525', hour=8, minute=30)
        for idx in range(10):
            csvfile, dta = _run(tmphome, cfgname, username, dta, idx, wr_old=True)
        system(f'cat {csvfile}')
        csvfile, dta = _run(tmphome, cfgname, username, dta, idx, wr_old=False)
        system(f'cat {csvfile}')


# pylint: disable=unknown-option-value
# pylint: disable=too-many-arguments,too-many-positional-arguments
def _run(tmphome, cfgname, username, dta, idx, wr_old):
    fin_start = run_start(cfgname, username, now=dta, defaultdt=dta)
    assert exists(fin_start)
    dta += timedelta(minutes=30)
    dct = run_stop(cfgname, username,
             get_ntcsv(f"{idx} time", None, None),
             dirhome=tmphome,
             now=dta, defaultdt=dta, wr_old=wr_old)
    csvfile = dct['fcsv']
    print(yellow(csvfile))
    print(yellow(dct['csvline']))
    return csvfile, dta


if __name__ == '__main__':
    test_stopat()
