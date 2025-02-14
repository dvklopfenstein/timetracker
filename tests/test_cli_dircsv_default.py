#!/usr/bin/env python3
"""Test the location of the csv file"""

#from os.path import isabs
from os.path import exists
#from os.path import join
from os.path import dirname
#from os.path import expanduser
from logging import basicConfig
from logging import DEBUG
#from logging import debug
from tempfile import TemporaryDirectory
#from timetracker.cli import Cli
from timetracker.cfg.finder import CfgFinder
from timetracker.cmd.init import run_init_test
from timetracker.cmd.start import run_start
from timetracker.cmd.stop import get_ntcsv
from timetracker.cmd.stop import run_stop
#from tests.pkgtttest.mkprojs import RELCSVS
from tests.pkgtttest.mkprojs import mk_projdirs
from tests.pkgtttest.mkprojs import findhome
from tests.pkgtttest.mkprojs import findhome_str
from tests.pkgtttest.mkprojs import prt_expdirs


basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'

def test_dircsv_default(project='pumpkin', username='carver'):
    """Test the location of the csv file"""

    obj = Obj(project, username, dircur='dirproj', dirgit=True)
    obj.run(dircsv="",   expcsv=f'proj/{project}/fname.csv')
    obj.run(dircsv=".",  expcsv=f'proj/{project}/fname.csv')
    obj.run(dircsv="..", expcsv='proj/fname.csv')
    obj.run(dircsv="~",  expcsv='fname.csv')

    dircsv = '.'
    curattr = 'dirproj'
    with TemporaryDirectory() as tmphome:
        exp = mk_projdirs(tmphome, project, dirgit=True)
        finder = CfgFinder(dircur=getattr(exp, curattr), trksubdir=None)
        cfgname = finder.get_cfgfilename()
        assert not exists(cfgname), findhome_str(exp.dirhome)
        cfgp, cfgg = run_init_test(cfgname, dircsv, project, exp.dirhome)
        #cfgp.set_filename_csv(join(
        assert cfgp
        findhome(tmphome)
        assert exists(cfgname), findhome_str(exp.dirhome)
        assert exists(cfgg.filename), findhome_str(exp.dirhome)
        assert dirname(dirname(cfgname)) == exp.dirproj
        assert dirname(cfgg.filename) == exp.dirhome
        fin_start = run_start(cfgname, username)
        assert fin_start, 'TODO'
        run_stop(cfgname, get_ntcsv('stopping', activity=None, tags=None))
        prt_expdirs(exp)

class Obj:
    """Test the location of the csv file"""
    # pylint: disable=too-few-public-methods

    def __init__(self, project, username, dircur, dirgit):
        self.project = project
        self.uname = username
        self.dircurattr = dircur
        self.dirgit = dirgit

    def run(self, dircsv, expcsv):
        """Run init w/dircsv, start, stop; Test location of csv"""

if __name__ == '__main__':
    test_dircsv_default()
