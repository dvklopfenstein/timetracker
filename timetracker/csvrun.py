"""Manage CSV file transition from old to new"""
# pylint: disable=duplicate-code

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import rename
from os.path import exists
from os.path import join
from shutil import copy
from csv import writer
from tempfile import TemporaryDirectory

from timetracker.csvfile import CsvFile as CsvFileNew
from timetracker.csvold  import CsvFile as CsvFileOld
from timetracker.csvutils import get_hdr


# pylint: disable=too-many-arguments
def wr_stopline(csvfilename, dta, delta, csvfields, dtz, wr_old=False):
    """Save csv in new format"""
    if wr_old:
        oldobj = CsvFileOld(csvfilename)
        return oldobj.wr_stopline(dta, dtz, delta, csvfields)

    newobj = CsvFileNew(csvfilename)
    if not exists(csvfilename):
        return newobj.wr_stopline(dta, delta, csvfields)
    hdr = get_hdr(csvfilename)
    if len(hdr) == 5:
        return newobj.wr_stopline(dta, delta, csvfields)
    return _wr_stopline(csvfilename, dta, delta, csvfields)

def _wr_stopline(csvfilename, dta, delta, csvfields):
    oldobj = CsvFileOld(csvfilename)
    with TemporaryDirectory() as tmpdir:
        fcsvtmp = join(tmpdir, 'file.csv')
        newobj = CsvFileNew(fcsvtmp)
        newobj.wr_hdrs()
        with open(fcsvtmp, 'w', encoding='utf8') as ocsv:
            for row in oldobj.get_data():
                writer(ocsv, lineterminator='\n').writerow(row)
            assert exists(fcsvtmp)
            data = [str(dta),
                    str(delta),
                    csvfields.activity, csvfields.message, csvfields.tags]
            writer(ocsv, lineterminator='\n').writerow(data)
            rename(csvfilename, f'{csvfilename}.bac')
            copy(fcsvtmp, csvfilename)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
