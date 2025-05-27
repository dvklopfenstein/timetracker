#!/usr/bin/env python3
"""Test the location of the csv file"""

from os.path import isabs
from os.path import exists
from os.path import join
from os.path import dirname
from logging import basicConfig
from logging import DEBUG
from logging import debug
from tempfile import TemporaryDirectory
from timetracker.utils import cyan
from timetracker.cfg.cfg import Cfg
from timetracker.cfg.cfg_global import get_cfgglobal
from timetracker.cfg.cfg_local import get_docproj
from timetracker.cmd.init import run_init
from timetracker.cmd.start import run_start
from timetracker.cmd.stop import run_stop
from timetracker.ntcsv import get_ntcsv
from tests.pkgtttest.mkprojs import findhome_str
from tests.pkgtttest.runfncs import proj_setup


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
            cfgname, finder, exp = proj_setup(tmphome, self.project, self.dircurattr, self.dirgit01)
            cfg = Cfg(cfgname)
            #exp = mk_projdirs(tmphome, self.project, self.dirgit01)
            #finder = CfgFinder(dircur=getattr(exp, self.dircurattr), trksubdir=None)
            #cfgname = finder.get_cfgfilename()
            #assert not exists(cfgname), findhome_str(exp.dirhome)

            # CMD: INIT; CFG PROJECT
            run_init(cfg, finder.dirgit, dircsv, self.project, dirhome=tmphome)
            cfgp = cfg.cfg_loc
            cfgg = get_cfgglobal(dirhome=tmphome)
            # pylint: disable=unsubscriptable-object
            # pylint: disable=protected-access
            ####assert get_docproj(cfgp.filename).csv_filename == join(dircsv, CfgProj.CSVPAT), \
            assert get_docproj(cfgp.filename).csv_filename == \
                   cfgp._assemble_csv_filepat(dircsv, self.project), (
                f'{get_docproj(cfgp.filename).csv_filename} != '
                f'{cfgp._assemble_csv_filepat(dircsv, self.project)}')
            exp_cfg_csv_fname = join(dircsv, fcsv)
            exp_cfg_csv_filename = _get_abscsv(exp.dirproj, dircsv, fcsv, tmphome)
            cfgp.set_filename_csv(exp_cfg_csv_fname)
            _chk_new_csv_filename(cfgp.filename, exp_cfg_csv_fname)
            #findhome(tmphome)
            assert exists(cfgname), findhome_str(exp.dirhome)
            assert exists(cfgg.filename), findhome_str(exp.dirhome)
            assert dirname(dirname(cfgname)) == exp.dirproj
            assert dirname(cfgg.filename) == exp.dirhome, \
                f'ACT({dirname(cfgg.filename)}) != EXP({exp.dirhome})'
            assert not exists(exp_cfg_csv_filename)

            # CMD: START
            ostart = run_start(cfgp, self.uname)
            assert exists(ostart.filename)
            assert not exists(exp_cfg_csv_filename)

            # CMD: STOP
            res = run_stop(cfgp,
                     self.uname,
                     get_ntcsv('stopping', activity=None, tags=None),
                     dirhome=tmphome)
            print(res)
            assert isabs(exp_cfg_csv_filename), f'SHOULD BE ABSPATH: {exp_cfg_csv_filename}'
            assert exists(exp_cfg_csv_filename), f'SHOULD EXIST: {exp_cfg_csv_filename}'
            assert not exists(ostart.filename), f'SHOULD NOT EXIST AFTER STOP: {ostart.filename}'

def _chk_new_csv_filename(glb_filename, exp_cfg_csv_fname):
    docproj = get_docproj(glb_filename)
    assert docproj is not None
    assert docproj.csv_filename == exp_cfg_csv_fname, \
        f'EXP({exp_cfg_csv_fname}) != ACT({docproj.csv_filename})'

def _get_abscsv(dirproj, dircsv, fcsv, tmphome):
    if '~' not in dircsv:
        return join(dirproj, dircsv, fcsv)
    return join(dircsv.replace('~', tmphome), fcsv)


if __name__ == '__main__':
    #test_dircsv_projdir()
    test_dircsv_projdoc()
