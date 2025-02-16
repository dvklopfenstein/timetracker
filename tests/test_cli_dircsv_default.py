#!/usr/bin/env python3
"""Test the location of the csv file"""

from os.path import isabs
from os.path import exists
from os.path import join
from os.path import dirname
#from os.path import normpath
#from os.path import expanduser
from logging import basicConfig
from logging import DEBUG
from logging import debug
from tempfile import TemporaryDirectory
#from timetracker.cli import Cli
from timetracker.utils import cyan
#from timetracker.utils import pink
from timetracker.cfg.finder import CfgFinder
from timetracker.cfg.cfg_local import CfgProj
from timetracker.cmd.init import run_init_test
from timetracker.cmd.start import run_start
from timetracker.cmd.stop import run_stop
from timetracker.cmd.stop import get_ntcsv
#from tests.pkgtttest.mkprojs import RELCSVS
from tests.pkgtttest.mkprojs import mk_projdirs
#from tests.pkgtttest.mkprojs import findhome
from tests.pkgtttest.mkprojs import findhome_str
#from tests.pkgtttest.mkprojs import prt_expdirs


basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'

def test_dircsv_projdir(project='pumpkin', username='carver'):
    """Test the location of the csv file when init from proj dir"""
    obj = Obj(project, username, dircur='dirproj', dirgit01=True)
    obj.run(dircsv="",   fcsv='fname.csv', expcsv=f'proj/{project}/fname.csv')
    obj.run(dircsv=".",  fcsv='fname.csv', expcsv=f'proj/{project}/fname.csv')
    obj.run(dircsv="..", fcsv='fname.csv', expcsv='proj/fname.csv')
    obj.run(dircsv="~",  fcsv='fname.csv', expcsv='fname.csv')

def test_dircsv_projdoc(project='pumpkin', username='carver'):
    """Test the location of the csv file when init from proj/doc dir"""
    obj = Obj(project, username, dircur='dirdoc', dirgit01=True)
    obj.run(dircsv="",   fcsv='fname.csv', expcsv=f'proj/{project}/fname.csv')
    obj.run(dircsv=".",  fcsv='fname.csv', expcsv=f'proj/{project}/fname.csv')
    obj.run(dircsv="..", fcsv='fname.csv', expcsv='proj/fname.csv')
    obj.run(dircsv="~",  fcsv='fname.csv', expcsv='fname.csv')

class Obj:
    """Test the location of the csv file"""
    # pylint: disable=too-few-public-methods

    def __init__(self, project, username, dircur, dirgit01):
        self.project = project
        self.uname = username
        self.dircurattr = dircur
        self.dirgit01 = dirgit01

    def run(self, dircsv, fcsv, expcsv):
        """Run init w/dircsv, start, stop; Test location of csv"""
        debug(cyan(f'\n{"="*100}'))
        debug(cyan(f'RUN: dircsv({dircsv}) csv({fcsv}) EXPCSV({expcsv})'))
        with TemporaryDirectory() as tmphome:
            exp = mk_projdirs(tmphome, self.project, self.dirgit01)
            finder = CfgFinder(dircur=getattr(exp, self.dircurattr), trksubdir=None)
            cfgname = finder.get_cfgfilename()
            assert not exists(cfgname), findhome_str(exp.dirhome)

            # CMD: INIT; CFG PROJECT
            cfgp, cfgg = run_init_test(cfgname, dircsv, self.project, exp.dirhome)
            # pylint: disable=unsubscriptable-object
            assert cfgp.read_doc()['csv']['filename'] == join(dircsv, CfgProj.CSVPAT)
            exp_cfg_csv_fname = join(dircsv, fcsv)
            exp_cfg_csv_filename = _get_abscsv(exp.dirproj, dircsv, fcsv, tmphome)
            cfgp.set_filename_csv(exp_cfg_csv_fname)
            assert cfgp.read_doc()['csv']['filename'] == exp_cfg_csv_fname
            #findhome(tmphome)
            assert exists(cfgname), findhome_str(exp.dirhome)
            assert exists(cfgg.filename), findhome_str(exp.dirhome)
            assert dirname(dirname(cfgname)) == exp.dirproj
            assert dirname(cfgg.filename) == exp.dirhome
            assert not exists(exp_cfg_csv_filename)

            # CMD: START
            fin_start = run_start(cfgname, self.uname)
            assert exists(fin_start)
            assert not exists(exp_cfg_csv_filename)

            # CMD: STOP
            run_stop(cfgname,
                     self.uname,
                     get_ntcsv('stopping', activity=None, tags=None),
                     dirhome=tmphome)
            assert isabs(exp_cfg_csv_filename), f'SHOULD BE ABSPATH: {exp_cfg_csv_filename}'
            assert exists(exp_cfg_csv_filename), f'SHOULD EXIST: {exp_cfg_csv_filename}'
            #prt_expdirs(exp)
            assert not exists(fin_start), f'SHOULD NOT EXIST AFTER STOP: {fin_start}'

def _get_abscsv(dirproj, dircsv, fcsv, tmphome):
    if '~' not in dircsv:
        return join(dirproj, dircsv, fcsv)
    return join(dircsv.replace('~', tmphome), fcsv)


if __name__ == '__main__':
    #test_dircsv_projdir()
    test_dircsv_projdoc()
