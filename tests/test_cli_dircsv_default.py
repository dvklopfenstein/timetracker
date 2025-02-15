#!/usr/bin/env python3
"""Test the location of the csv file"""

#from os.path import isabs
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

def test_dircsv_default(project='pumpkin', username='carver'):
    """Test the location of the csv file"""

    obj = Obj(project, username, dircur='dirproj', dirgit01=True)
    obj.run(dircsv="",   fcsv='fname.csv', expcsv=f'proj/{project}/fname.csv')
    obj.run(dircsv=".",  fcsv='fname.csv', expcsv=f'proj/{project}/fname.csv')
    obj.run(dircsv="..", fcsv='fname.csv', expcsv='proj/fname.csv')
    obj.run(dircsv="~",  fcsv='fname.csv', expcsv='fname.csv')

    #obj = Obj(project, username, dircur='dirdoc', dirgit01=True)
    #obj.run(dircsv="",   expcsv=f'proj/{project}/fname.csv')
    #obj.run(dircsv=".",  expcsv=f'proj/{project}/fname.csv')
    #obj.run(dircsv="..", expcsv='proj/fname.csv')
    #obj.run(dircsv="~",  expcsv='fname.csv')

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
            cfg_csv_filename = join(dircsv, fcsv)
            cfgp.set_filename_csv(cfg_csv_filename)
            assert cfgp.read_doc()['csv']['filename'] == join(dircsv, fcsv)
            #findhome(tmphome)
            assert exists(cfgname), findhome_str(exp.dirhome)
            assert exists(cfgg.filename), findhome_str(exp.dirhome)
            assert dirname(dirname(cfgname)) == exp.dirproj
            assert dirname(cfgg.filename) == exp.dirhome

            # CMD: START
            fin_start = run_start(cfgname, self.uname)
            assert exists(fin_start)

            # CMD: STOP
            run_stop(cfgname, get_ntcsv('stopping', activity=None, tags=None))
            #prt_expdirs(exp)


if __name__ == '__main__':
    test_dircsv_default()
