#!/usr/bin/env python3
"""Test the TimeTracker project config dir finder"""

from os.path import isabs
from os.path import join
from os.path import expanduser
from logging import basicConfig
from logging import DEBUG
from timetracker.cfg.utils import get_abspath
from timetracker.cfg.utils import get_relpath


basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'

def test_csvloc():
    """Test the TimeTracker project config dir finder"""
    relcsvs = [
        "filename.csv",
        "./filename.csv",
        "../filename.csv",
        "~/filename.csv",
    ]
    print(f"{SEP}Test identifying relative paths")
    for csv in relcsvs:
        assert not isabs(csv)

    print(f"{SEP}Test identifying absolute paths")
    absdirproj = '/home/user/me/proj/apples'
    assert isabs(absdirproj)

    print("\n= TEST get_abspath & get_relpath =================================================")
    for cfgcsv_orig, abs_exp, rel_exp in zip(relcsvs, _exp_abscsv_clean(), _exp_relcsv_clean()):
        cfgcsv_abs = get_abspath(cfgcsv_orig, absdirproj)
        assert cfgcsv_abs == abs_exp
        cfgcsv_rel = get_relpath(cfgcsv_abs, absdirproj)
        assert cfgcsv_rel == rel_exp
        print(f'{cfgcsv_orig:>15} {cfgcsv_abs:38} {cfgcsv_rel}')


def _exp_abscsv_clean():
    return [
        '/home/user/me/proj/apples/filename.csv',
        '/home/user/me/proj/apples/filename.csv',
        '/home/user/me/proj/filename.csv',
        join(expanduser("~"), 'filename.csv')]

def _exp_relcsv_clean():
    return [
        'filename.csv',
        'filename.csv',
        '../filename.csv',
        '~/filename.csv']


if __name__ == '__main__':
    test_csvloc()
