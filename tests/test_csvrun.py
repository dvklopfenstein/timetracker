#!/usr/bin/env python3
"""Test `trk stop --at`"""

from os import system
from os.path import exists
#from logging import basicConfig
#from logging import DEBUG
from datetime import timedelta
from tempfile import TemporaryDirectory
from timetracker.utils import yellow
from timetracker.ntcsv import get_ntcsv
from timetracker.cfg.cfg import Cfg
from timetracker.cmd.init import run_init
from timetracker.cmd.start import run_start
from timetracker.cmd.stop import run_stop
from timetracker.csvutils import get_hdr
from timetracker.csvold import CsvFile as CsvFileOld
from timetracker.csvfile import CsvFile as CsvFileNew
from tests.pkgtttest.dts import get_dt
from tests.pkgtttest.runfncs import proj_setup


def test_stopat(project='pumpkin', username='carver', dircsv=None):
    """Test rewriting csv file"""
    #basicConfig(level=DEBUG)

    with TemporaryDirectory() as tmphome:
        cfgname, finder, _ = proj_setup(tmphome, project, dircur='dirproj', dirgit01=True)
        cfg = Cfg(cfgname)
        run_init(cfg, finder.dirgit, dircsv, project, dirhome=tmphome)  # cfgg
        assert cfgname == cfg.cfg_loc.filename, f'{cfgname} != {cfg.cfg_loc.filename}'

        # Write in old format
        dta = get_dt(yearstr='2525', hour=8, minute=30)
        for idx in range(10):
            csvfile, dta = _run(tmphome, cfg.cfg_loc, username, dta, idx, wr_old=True)
        system(f'cat {csvfile}')
        olddata = CsvFileOld(csvfile).get_ntdata()
        for e in olddata:
            print(e)

        # Update to the new format, upon adding a new time slot (time 10)
        csvfile, dta = _run(tmphome, cfg.cfg_loc, username, dta, idx+1, wr_old=False)
        system(f'cat {csvfile}')
        _chk(csvfile, olddata)


def _chk(csvfile, olddata):
    csvnew = CsvFileNew(csvfile)
    # Check new header
    assert get_hdr(csvfile) == csvnew.hdrs, \
        f'EXP != ACT:\nEXP({csvnew.hdrs})\nACT({get_hdr(csvfile)})'

    # Check data length
    newdata, errs = csvnew.get_ntdata()
    print(f'CONFIGFILE READ ERRORS: {errs}')
    assert len(olddata) == len(newdata) - 1, \
        f'LEN EXP({len(olddata)}) != ACT({len(newdata)})\n'

    # Check data
    for ntold, ntnew in zip(olddata, newdata):
        print('OLD:', ntold)
        print('NEW:', ntnew)
        assert ntold == ntnew, f'EXP != ACT\nOLD({ntold})\nNEW({ntnew})'
    print(newdata[-1])
    assert newdata[-1].message == '10 time'

# pylint: disable=unknown-option-value
# pylint: disable=too-many-arguments,too-many-positional-arguments
def _run(tmphome, cfgproj, username, dta, idx, wr_old):
    ostart = run_start(cfgproj, username, now=dta, defaultdt=dta)
    assert exists(ostart.filename)
    dta += timedelta(minutes=30)
    dct = run_stop(cfgproj, username,
             get_ntcsv(f"{idx} time", None, None),
             dirhome=tmphome,
             now=dta, defaultdt=dta, wr_old=wr_old)
    csvfile = dct['fcsv']
    print(yellow(csvfile))
    print(yellow(dct['csvline']))
    return csvfile, dta


if __name__ == '__main__':
    test_stopat()
