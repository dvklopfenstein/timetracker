#!/usr/bin/env python3
"""Test to explore how os.path works with relative & absolute paths"""

from os.path import isabs
from os.path import join
from os.path import abspath
from os.path import relpath
from os.path import normpath
from os.path import expanduser
from logging import basicConfig
from logging import DEBUG
from tests.pkgtttest.mkprojs import RELCSVS


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
    relcsvs = RELCSVS
    print(f"{SEP}isabs on various relative filenames")
    for csv in relcsvs:
        assert not isabs(csv)

    print(f"{SEP}Test identifying absolute paths")
    absdirhome = '/home/user/me/'
    absdirproj = join(absdirhome, 'proj/apples')

    abscsvs_messy = _get_abscsv_messy(absdirproj, relcsvs) # join or expanduser
    for absmessy, exp in zip(abscsvs_messy, _exp_abscsv_messy()):
        assert absmessy == exp, f'\nACT={absmessy}\nEXP={exp}'

    _run_abspath(relcsvs, abscsvs_messy)
    _run_relpath(relcsvs, absdirproj, abscsvs_messy)

def _run_abspath(relcsvs, abscsvs_messy):
    """Get csv abspath"""
    print("\n= TEST abspath(filenamecsv, dirproj) =======================================")
    for relcsv, abscsv_messy, abscsv_exp in zip(relcsvs, abscsvs_messy, _exp_abscsv_clean()):
        abscsv_clean = abspath(abscsv_messy)
        if '~' in abscsv_clean:
            abscsv_clean = expanduser(abscsv_clean)
        print(f'{relcsv:>15} {abscsv_messy:41} {abscsv_clean}')
        assert abscsv_clean == abscsv_exp, f'\nEXP: {abscsv_exp}\nACT: {abscsv_clean}'

def _run_relpath(relcsvs, absdirproj, abscsvs_messy):
    """Get csv relpath; relative to project directory """
    print("\n= TEST 4 =======================================================================")
    print(f"Get csv relative to project dir, {absdirproj}")
    print(f"HOME DIR: {expanduser('~')}")
    print("relpath         join('/home/user/me/proj', relpath)       "
          "os.path.abspath(absmessy)                relclean")
    print("--------------- ----------------------------------------  "
          "--------------------------------------   ------------")
    for cfgcsv_orig, abscsv_messy, relcsv_exp in zip(relcsvs, abscsvs_messy, _exp_relcsv_clean()):
        relcsv_clean = relpath(abscsv_messy, absdirproj)
        if '~' in abscsv_messy:
            relcsv_clean = expanduser(relcsv_clean)
        print(f'{cfgcsv_orig:>15} {abscsv_messy:41} {abspath(abscsv_messy):40} {relcsv_clean}')
        if '~' in abscsv_messy:
            assert relcsv_clean == relcsv_exp, f'\nEXP: {relcsv_exp}\nACT: {relcsv_clean}'


def _get_abscsv_messy(absdirproj, relcsvs):
    abscsvs_messy = []
    for relcsv in relcsvs:
        if '~' not in relcsv:
            abscsvs_messy.append(join(absdirproj, relcsv))
        else:
            assert relcsv[:1] == '~'
            abscsvs_messy.append(expanduser(relcsv))
    return abscsvs_messy

def _exp_abscsv_messy():
    return [
        '/home/user/me/proj/apples/filename.csv',
        '/home/user/me/proj/apples/./filename.csv',
        '/home/user/me/proj/apples/../filename.csv',
        join(expanduser("~"), 'filename.csv')]

def _exp_abscsv_clean():
    return [
        '/home/user/me/proj/apples/filename.csv',
        '/home/user/me/proj/apples/filename.csv',
        '/home/user/me/proj/filename.csv',
        normpath(join(expanduser("~"), 'filename.csv'))]

def _exp_relcsv_clean():
    return [
        'filename.csv',
        'filename.csv',
        '../filename.csv',
        '../../../../filename.csv']


if __name__ == '__main__':
    test_csvloc()
