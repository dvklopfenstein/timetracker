#!/usr/bin/env python3
"""Test to explore how os.path works with relative & absolute paths"""

#from os.path import isabs
from os.path import join
#from os.path import abspath
#from os.path import relpath
#from os.path import normpath
from os.path import exists
#from os.path import expanduser
from logging import basicConfig
from logging import DEBUG
from tempfile import TemporaryDirectory
from timetracker.cfg.cfg_local import CfgProj
#from tests.pkgtttest.mkprojs import RELCSVS
from tests.pkgtttest.mkprojs import mk_projdirs
from tests.pkgtttest.mkprojs import findhome_str


basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'

def test_csvloc():
    """Test to explore how os.path works with relative & absolute paths"""
    #relcsvs = [
    #    "filename.csv",
    #    "./filename.csv",
    #    "../filename.csv",
    #    "~/filename.csv",
    #]
    with TemporaryDirectory() as tmphome:
        _run_plain(tmphome)

def _run_plain(tmphome, project='apple', name='picker'):
    #relcsvs = RELCSVS

    expdirs = mk_projdirs(tmphome, project)
    # exists(1) dirhome        /tmp/tmpp9wcmtg2
    # exists(1) dirproj        /tmp/tmpp9wcmtg2/proj/apple
    # exists(.) dirgit         None
    # exists(1) dirdoc         /tmp/tmpp9wcmtg2/proj/apple/doc
    # exists(0) cfglocfilename /tmp/tmpp9wcmtg2/proj/apple/.timetracker/config
    assert not exists(expdirs.cfglocfilename)
    cfgproj = CfgProj(expdirs.cfglocfilename)
    cfgproj.wr_ini_file(project)
    _chk('plain',
         act=cfgproj.get_filename_csv(name),
         exp=join(expdirs.dirproj, f'timetracker_{project}_{name}.csv'))
    print(findhome_str(tmphome, '-type f'))

def _chk(msg, act, exp):
    assert act == exp, f'{msg}\nEXP: {exp}\nACT: {act}'


if __name__ == '__main__':
    test_csvloc()
