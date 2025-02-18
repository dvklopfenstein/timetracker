#!/usr/bin/env python3
"""Test the TimeTracker project config dir finder"""

from os import makedirs
from os.path import exists
from os.path import dirname
from os.path import join
from logging import basicConfig
from logging import DEBUG
from tempfile import TemporaryDirectory
from timetracker.cfg.finder import CfgFinder
from tests.pkgtttest.mkprojs import mkdirs
from tests.pkgtttest.mkprojs import findhome
from tests.pkgtttest.cmpstr import str_get_dirtrk


basicConfig(level=DEBUG)

SEP1 = f'\n{"="*80}\n'
SEP2 = f'{"-"*80}\n'

def test_cfgbase_temp(trksubdir='.timetracker'):
    """Test the TimeTracker project config dir finder"""
    print(f'{SEP1}1) INITIALIZE "HOME" DIRECTORY')
    # Test finder when current directory is NOT time-tracked
    with TemporaryDirectory() as tmp_home:
        proj2wdir = mkdirs(tmp_home)
        findhome(tmp_home)

    # Test finder when current directory is NOT time-tracked
    print(f'{SEP1}  NO .timetracker  NO .git')
    with TemporaryDirectory() as tmp_home:
        proj2wdir = mkdirs(tmp_home)
        _test_tracked0_git0(proj2wdir, trksubdir)

    # Test finder when current directory is NOT time-tracked and is NOT git-tracked
    print(f'{SEP1} YES .timetracker  NO .git')
    with TemporaryDirectory() as tmp_home:
        proj2wdir = mkdirs(tmp_home)
        _test_tracked1_git0(proj2wdir, trksubdir)

    # Test finder when current directory is NOT time-tracked and is NOT git-tracked
    print(f'{SEP1}  NO .timetracker YES .git')
    with TemporaryDirectory() as tmp_home:
        proj2wdir = mkdirs(tmp_home)
        _test_tracked0_git1(proj2wdir, trksubdir)

    # Test finder when current directory IS time-tracked AND IS git-tracked
    print(f'{SEP1} YES .timetracker YES .git')
    with TemporaryDirectory() as tmp_home:
        proj2wdir = mkdirs(tmp_home)
        _test_tracked1_git1(proj2wdir, trksubdir)


def _test_tracked0_git0(proj2wdir, trksubdir):
    """Test Finder when proj/.timetracker directory does not exist"""
    for proj, dirproj in proj2wdir.items():
        dirtrk_exp = join(dirproj, trksubdir)
        dirgit_exp = join(dirproj, '.git')
        _msg_exists(proj, dirproj, dirtrk_exp, dirgit_exp)

        dircur = dirproj
        finder = CfgFinder(dircur=dircur, trksubdir=trksubdir)
        print(f'{proj:11} TEST {finder.get_desc()}')
        assert finder.dirtrk is None
        assert finder.dirproj == dirproj
        assert finder.get_dirgit() is None
        assert finder.project == proj, f'PROJ EXP({proj}) != ACT({finder.project})'
        assert finder.get_dirtrk() == dirtrk_exp, str_get_dirtrk(dirtrk_exp, finder)
        assert finder.get_dircsv_default() == '.', ('t0g0 DIRCSV '
            f'ACT({finder.get_dircsv_default()}) != EXP({dirname(dirtrk_exp)})')

        dircur = join(dirproj, 'doc')
        finder = CfgFinder(dircur=dircur, trksubdir=trksubdir)
        print(f'{proj:11} TEST {finder.get_desc()}')
        assert finder.dirtrk is None, str(finder)
        assert finder.dirproj == dircur, f't0g0 DIRPOJ EXP({dirproj}) != ACT({finder.dirproj})'
        assert finder.get_dirgit() is None
        assert finder.project == 'doc', f't0g0 PROJ EXP({proj}) != ACT({finder.project})'
        assert finder.get_dirtrk() == join(dircur, trksubdir), f't0g0 {dircur}\n{str(finder)}'
        # pylint: disable=line-too-long
        assert finder.get_dircsv_default() == '.', ('t0g0 DIRCSV '
            f'ACT({finder.get_dircsv_default()}) != EXP({dirname(dirtrk_exp)})')

def _test_tracked1_git0(proj2wdir, trksubdir):
    """Test Finder when proj/.timetracker directory exists"""
    for proj, dirproj in proj2wdir.items():
        dirtrk_exp = join(dirproj, trksubdir)
        dirgit_exp = join(dirproj, '.git')
        makedirs(dirtrk_exp)
        _msg_exists(proj, dirproj, dirtrk_exp, dirgit_exp)

        dircur = dirproj
        finder = CfgFinder(dircur=dircur, trksubdir=trksubdir)
        print(f'{proj:11} TEST {finder.get_desc()}')
        assert finder.dirtrk == dirtrk_exp, str_get_dirtrk(dirtrk_exp, finder)
        assert finder.dirproj == dirproj
        assert finder.get_dirgit() is None
        assert finder.project == proj, f'PROJ EXP({proj}) != ACT({finder.project})'
        assert finder.get_dirtrk() == dirtrk_exp
        assert finder.get_dircsv_default() == '.', ('t1g0 DIRCSV '
            f'ACT({finder.get_dircsv_default()}) != EXP({dirname(dirtrk_exp)})')

        dircur = join(dirproj, 'doc')
        finder = CfgFinder(dircur=dircur, trksubdir=trksubdir)
        print(f'{proj:11} TEST {finder.get_desc()}')
        assert finder.dirtrk == dirtrk_exp, str_get_dirtrk(dirtrk_exp, finder)
        assert finder.dirproj == dirproj
        assert finder.get_dirgit() is None
        assert finder.project == proj, f'PROJ EXP({proj}) != ACT({finder.project})'
        assert finder.get_dirtrk() == dirtrk_exp, f"\nEXP: {dirtrk_exp}\nACT: {str(finder)}"
        assert finder.get_dircsv_default() == dirproj

def _test_tracked0_git1(proj2wdir, trksubdir):
    """Test Finder when proj/.timetracker directory does not exist"""
    for proj, dirproj in proj2wdir.items():
        dirtrk_exp = join(dirproj, trksubdir)
        dirgit_exp = join(dirproj, '.git')
        makedirs(dirgit_exp)
        _msg_exists(proj, dirproj, dirtrk_exp, dirgit_exp)

        dircur = dirproj
        finder = CfgFinder(dircur=dircur, trksubdir=trksubdir)
        print(f'{proj:11} TEST {finder.get_desc()}')
        assert finder.dirtrk is None
        assert finder.dirproj == dirproj
        # pylint: disable=line-too-long
        assert finder.get_dirgit() == dirgit_exp, f'GIT EXP({dirgit_exp}) ACT({finder.get_dirgit()})'
        assert finder.project == proj, f'PROJ EXP({proj}) != ACT({finder.project})'
        assert finder.get_dirtrk() == dirtrk_exp, str_get_dirtrk(dirtrk_exp, finder)
        assert finder.get_dircsv_default() == '.', ('t0g1 DIRCSV '
            f'ACT({finder.get_dircsv_default()}) != EXP(".")')

        dircur = join(dirproj, 'doc')
        finder = CfgFinder(dircur=dircur, trksubdir=trksubdir)
        print(f'{proj:11} TEST {finder.get_desc()}')
        assert finder.dirtrk is None, str(finder)
        assert finder.dirproj == dirproj
        assert finder.get_dirgit() == dirgit_exp
        assert finder.project == proj, f'PROJ EXP({proj}) != ACT({finder.project})'
        assert finder.get_dirtrk() == dirtrk_exp, str_get_dirtrk(dirtrk_exp, finder)
        assert finder.get_dircsv_default() == dirproj, ('t0g1 DIRCSV '
            f'ACT({finder.get_dircsv_default()}) != EXP({dirname(dirgit_exp)})')

def _test_tracked1_git1(proj2wdir, trksubdir):
    """Test Finder when proj/.timetracker directory does not exist"""
    for proj, dirproj in proj2wdir.items():
        dirtrk_exp = join(dirproj, trksubdir)
        dirgit_exp = join(dirproj, '.git')
        makedirs(dirtrk_exp)
        makedirs(dirgit_exp)
        _msg_exists(proj, dirproj, dirtrk_exp, dirgit_exp)

        dircur = dirproj
        finder = CfgFinder(dircur=dircur, trksubdir=trksubdir)
        print(f'{proj:11} TEST {finder.get_desc()}')
        assert finder.dirtrk == dirtrk_exp, str_get_dirtrk(dirtrk_exp, finder)
        assert finder.dirproj == dirproj
        assert finder.get_dirgit() == dirgit_exp
        assert finder.project == proj, f'PROJ EXP({proj}) != ACT({finder.project})'
        assert finder.get_dirtrk() == dirtrk_exp
        assert finder.get_dircsv_default() == '.', ('t0g1 DIRCSV '
            f'ACT({finder.get_dircsv_default()}) != EXP(".")')

        dircur = join(dirproj, 'doc')
        finder = CfgFinder(dircur=dircur, trksubdir=trksubdir)
        print(f'{proj:11} TEST {finder.get_desc()}')
        assert finder.dirtrk == dirtrk_exp, str_get_dirtrk(dirtrk_exp, finder)
        assert finder.dirproj == dirproj
        assert finder.get_dirgit() == dirgit_exp
        assert finder.project == proj, f'PROJ EXP({proj}) != ACT({finder.project})'
        assert finder.get_dirtrk() == dirtrk_exp, f"\nEXP: {dirproj}\nACT: {str(finder)}"
        assert finder.get_dircsv_default() == dirproj

def _msg_exists(proj, dirproj, dirtrk, dirgit=None):
    print(f'{SEP2}{proj:11} PROJECT:     exists({int(exists(dirproj))}) {dirproj}')
    print(f'{proj:11} DIR TRACKER: exists({int(exists(dirtrk))}) {dirtrk}')
    if dirgit is not None:
        print(f'{proj:11} DIR GIT:     exists({int(exists(dirgit))}) {dirgit}')


if __name__ == '__main__':
    test_cfgbase_temp()
