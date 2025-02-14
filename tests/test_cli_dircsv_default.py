#!/usr/bin/env python3
"""Test the TimeTracker project config dir finder"""
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
    """Test the TimeTracker project config dir finder"""
    #relcsvs = [
    #    "filename.csv",
    #    "./filename.csv",
    #    "../filename.csv",
    #    "~/filename.csv",
    #]
    #relcsvs = RELCSVS

    #cli = Cli(['init'])
    #cli = Cli(['csvupdate'])

    dircsv = '.'
    with TemporaryDirectory() as tmphome:
        exp = mk_projdirs(tmphome, project, dirgit=True)
        finder = CfgFinder(exp.dirproj, trksubdir=None)
        cfgname = finder.get_cfgfilename()
        assert not exists(cfgname), findhome_str(exp.dirhome)
        cfgp, cfgg = run_init_test(cfgname, dircsv, project, exp.dirhome)
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
    #    _run_proj_cur_same(relcsvs, exp.dirproj)
    #    _run_proj_cur_diff(relcsvs, exp.dirdoc)

#def _run_proj_cur_same(relcsvs, dircur, project):
#    print("\n= TEST finder.get_dircsv_default() ================")
#    files = zip(relcsvs, _exp_abscsv_clean(project), _exp_relcsv_clean())
#    for cfgcsv_orig, abs_exp, rel_exp in files:
#        cli = Cli()
#        dflt = cli._get_csvfilename_dflt()
#        print(f'{dflt} {cfgcsv_orig:>17} {abs_exp:39} {rel_exp}')
#        assert dflt == '.'
#
#def _run_proj_cur_diff(relcsvs, dircur):
#    print("\n= TEST finder.get_dircsv_default() ================")
#    files = zip(relcsvs, _exp_abscsv_clean(), _exp_relcsv_clean())
#    for cfgcsv_orig, abs_exp, rel_exp in files:
#        cli = Cli()
#        dflt = cli._get_csvfilename_dflt()
#        print(f'{dflt} {cfgcsv_orig:>17} {abs_exp:39} {rel_exp}')
#        assert dflt == '.'


#def _exp_abscsv_clean(project):
#    return [
#        f'/home/user/me/proj/{project}/filename.csv',
#        f'/home/user/me/proj/{project}/filename.csv',
#        '/home/user/me/proj/filename.csv',
#        join(expanduser("~"), 'filename.csv')]
#
#def _exp_relcsv_clean():
#    return [
#        'filename.csv',
#        'filename.csv',
#        '../filename.csv',
#        '~/filename.csv']


if __name__ == '__main__':
    test_dircsv_default()
