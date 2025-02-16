#!/usr/bin/env python3
"""Test the TimeTracker project config dir finder"""

from os.path import isabs
from os.path import join
from logging import basicConfig
from logging import DEBUG
from timetracker.cfg.utils import get_abspath
from timetracker.cfg.utils import get_relpath
from tests.pkgtttest.mkprojs import RELCSVS


basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'

def test_csvloc():
    """Test the TimeTracker project config dir finder"""
    #relcsvs = [
    #    "filename.csv",
    #    "./filename.csv",
    #    "../filename.csv",
    #    "~/filename.csv",
    #]
    relcsvs = RELCSVS

    # ==========================================================
    print(f"{SEP}Test identifying absolute path")
    absdirhome = '/home/user/me'
    absdirproj = '/home/user/me/proj/apples'
    assert isabs(absdirproj)

    # ==========================================================
    print(f"{SEP}Test identifying relative paths")
    for csv in relcsvs:
        assert not isabs(csv)

    # ==========================================================
    print(f"{SEP}Test get_abspath")
    for csv, abs_exp in zip(relcsvs, _exp_abscsv_clean(absdirhome)):
        abs_act = get_abspath(csv, absdirproj, absdirhome)
        print(f'TEST: {csv:>15}=ORIG ACT={abs_act:38} EXP={abs_exp}')

    # ==========================================================
    print(f"{SEP}Test get_relpath")
    for csv, rel_exp in zip(relcsvs, _exp_relcsv_clean()):
        rel_act = get_relpath(get_abspath(csv, absdirproj, absdirhome), absdirproj, absdirhome)
        print(f'TEST: ORIG({csv:>15}) ACT={rel_act:38} EXP={rel_exp}')

    # ==========================================================
    print(f"{SEP}TEST get_abspath & get_relpath")
    files = zip(relcsvs, _exp_abscsv_clean(absdirhome), _exp_relcsv_clean())
    for cfgcsv_orig, abs_exp, rel_exp in files:
        cfgcsv_abs = get_abspath(cfgcsv_orig, absdirproj, absdirhome)
        cfgcsv_rel = get_relpath(cfgcsv_abs,  absdirproj, absdirhome)
        print(f'TEST: ORIG({cfgcsv_orig:>15}) ABS={cfgcsv_abs:38} REL={cfgcsv_rel}')
        # pylint: disable=line-too-long
        assert cfgcsv_abs == abs_exp, f'ABS FAILED:\nORIG: {cfgcsv_orig}\nEXP:  {abs_exp}\nACT:  {cfgcsv_abs}'
        assert cfgcsv_rel == rel_exp, f'REL FAILED:\nORIG: {cfgcsv_orig}\nEXP:  {rel_exp}\nACT:  {cfgcsv_rel}'


def _exp_abscsv_clean(dirhome):
    return [
        '/home/user/me/proj/apples/filename.csv',
        '/home/user/me/proj/apples/filename.csv',
        '/home/user/me/proj/filename.csv',
        join(dirhome, 'filename.csv')]

def _exp_relcsv_clean():
    return [
        'filename.csv',
        'filename.csv',
        '../filename.csv',
        '~/filename.csv']


if __name__ == '__main__':
    test_csvloc()
