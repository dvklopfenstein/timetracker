#!/usr/bin/env python3
"""Test the TimeTracker project config dir finder"""

#from os import makedirs
from os.path import exists
from os.path import isabs
from os.path import join
from os.path import abspath
from os.path import relpath
from os.path import expanduser
from logging import basicConfig
from logging import DEBUG
from tempfile import TemporaryDirectory
#from timetracker.cfg.finder import CfgFinder
from tests.pkgtttest.mkprojs import mk_projdirs_wcfgs
from tests.pkgtttest.mkprojs import findhome
#from tests.pkgtttest.cmpstr import str_get_dirtrk


basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'

def test_csvloc(trksubdir='.timetracker'):
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
    absdirhome = '/home/user/me/'
    absdirproj = join(absdirhome, 'proj/apples')
    absdircsvs = join(absdirhome, 'csvs')
    abscsvs = []
    for relcsv in relcsvs:
        abscsv = join(absdirproj, relcsv)
        assert isabs(abscsv)
        abscsvs.append(abscsv)

    print(f"{SEP}Get csv abspath")
    for relcsv, abscsv_messy in zip(relcsvs, abscsvs):
        abscsv_clean = abspath(abscsv_messy)
        if '~' in abscsv:
            abscsv_clean = expanduser(abscsv_clean)
        print(f'{relcsv:>15} {abscsv_messy:41} {abscsv_clean}')

    print(f"{SEP}Get csv relative to project dir, {absdirproj}")
    for relcsv, abscsv_messy in zip(relcsvs, abscsvs):
        relcsv_clean = relpath(abscsv_messy, absdirproj)
        if '~' in abscsv:
            relcsv_clean = expanduser(relcsv_clean)
        print(f'{relcsv:>15} {abscsv_messy:41} {relcsv_clean:>24} {abspath(abscsv_messy)}')



if __name__ == '__main__':
    test_csvloc()
