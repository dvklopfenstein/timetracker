#!/usr/bin/env python3
"""Test the TimeTracker global configuration"""

from os import makedirs
from os.path import exists
from os.path import join
from subprocess import run
from logging import basicConfig
from logging import DEBUG
from logging import debug
from tempfile import TemporaryDirectory
from timetracker.cfg.finder import CfgFinder


basicConfig(level=DEBUG)

SEP1 = f'\n{"="*80}\n'

def test_cfgbase_temp(trksubdir='.timetracker'):
    """Test cfg flow"""
    print(f'{SEP1}1) INITIALIZE "HOME" DIRECTORY')
    with TemporaryDirectory() as tmp_home:
        proj2wdir = _mk_dirs(tmp_home)
        _find(tmp_home)

        # Test finder when current directory is NOT time-tracked
        _test_tracked0(proj2wdir, trksubdir)
        # Test finder when current directory IS time-tracked
        _test_tracked1(proj2wdir, trksubdir)

def _test_tracked0(proj2wdir, trksubdir):
    for proj, dirproj in proj2wdir.items():
        dirtrk = join(dirproj, trksubdir)
        print(f'{SEP1}{proj:11} PROJECT:     exists({int(exists(dirproj))}) {dirproj}')
        print(f'{proj:11} DIR CURRENT: exists({int(exists(dirtrk))}) {dirtrk}')

        dircur = dirproj
        finder = CfgFinder(dircur=dircur, trksubdir=trksubdir)
        print(f'{proj:11} TEST {finder}')
        assert finder.dirtrk is None
        assert finder.project == proj, f'PROJ EXP({proj}) != ACT({finder.project})'
        assert finder.get_dirtrk() == dircur

        dircur = join(dirproj, 'doc')
        finder = CfgFinder(dircur=dircur, trksubdir=trksubdir)
        print(f'{proj:11} TEST {finder}')
        assert finder.dirtrk is None, str(finder)
        assert finder.project == 'doc', f'PROJ EXP({proj}) != ACT({finder.project})'
        assert finder.get_dirtrk() == dircur, str(finder)

def _test_tracked1(proj2wdir, trksubdir):
    for proj, dirproj in proj2wdir.items():
        dirtrk = join(dirproj, trksubdir)
        makedirs(dirtrk)

        print(f'{SEP1}{proj:11} PROJECT:     exists({int(exists(dirproj))}) {dirproj}')
        print(f'{proj:11} DIR CURRENT: exists({int(exists(dirtrk))}) {dirtrk}')

        dircur = dirproj
        finder = CfgFinder(dircur=dircur, trksubdir=trksubdir)
        print(f'{proj:11} TEST {finder}')
        assert finder.dirtrk == dirtrk, str(finder)
        assert finder.project == proj, f'PROJ EXP({proj}) != ACT({finder.project})'
        assert finder.get_dirtrk() == dirtrk

        dircur = join(dirproj, 'doc')
        finder = CfgFinder(dircur=dircur, trksubdir=trksubdir)
        print(f'{proj:11} TEST {finder}')
        assert finder.dirtrk == dirtrk, str(finder)
        assert finder.project == proj, f'PROJ EXP({proj}) != ACT({finder.project})'
        assert finder.get_dirtrk() == dirtrk, str(finder)


def _mk_dirs(tmp_home):
    projs = {
        'apples'      : join(tmp_home, 'proj/apples'),
        'blueberries' : join(tmp_home, 'proj/blueberries'),
        'cacao'       : join(tmp_home, 'proj/cacao'),
    }
    for pdir in projs.values():
        dirdoc = join(pdir, 'doc')
        makedirs(dirdoc)
    return projs

def _find(home):
    debug(run(f'find {home}'.split(), capture_output=True, text=True, check=True).stdout)

if __name__ == '__main__':
    #test_dirhome()
    #test_cfgbase_home()
    test_cfgbase_temp()
