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

from timetracker.ntcsv import get_ntcsv
from timetracker.csvfile import CsvFile as CsvFileNew
from timetracker.csvold  import CsvFile as CsvFileOld
from timetracker.csvutils import get_hdr


# pylint: disable=unknown-option-value
# pylint: disable=too-many-arguments,too-many-positional-arguments
def wr_stopline(csvfilename, dta, delta, csvfields, dtz, wr_old=False):
    """Save csv in new format"""
    if csvfields is None:
        csvfields = get_ntcsv('NO MESSAGE GIVEN', None, None)
    if wr_old:
        #print('AAAAA INTENTIONALLY MAKING ORIG FMT AAA')
        oldobj = CsvFileOld(csvfilename)
        return oldobj.wr_stopline(dta, dtz, delta, csvfields)

    #print('BBBBB CHECKING CSV FORMAT BBBBBBBBBBBBB')
    newobj = CsvFileNew(csvfilename)
    if not exists(csvfilename):
        #print('CCCCC CREATING NEW CSV CCCCCCCCCCCCCCCC')
        return newobj.wr_stopline(dta, delta, csvfields)
    hdr = get_hdr(csvfilename)
    #print('DDDDD CHECKING HDR FOR FORMAT DDDDDDDDD')
    if len(hdr) == 5:
        #print('EEEEE FOUND NEW FORMAT EEEEEEEEEEEEEEEE')
        return newobj.wr_stopline(dta, delta, csvfields)
    #print('FFFFF FOUND ORIG FORMAT FFFFFFFFFFFFFFF')
    convert_csv(csvfilename)
    return newobj.wr_stopline(dta, delta, csvfields)

def chk_n_convert(fcsv):
    """Check & if needed, convert the original csv format to new concise format"""
    if not exists(fcsv):
        return
    if len(get_hdr(fcsv)) == 5:
        return
    print(len(get_hdr(fcsv)), 'HHHHHHHHHHHHHHHHHHHHHHHHHH', get_hdr(fcsv), fcsv)
    convert_csv(fcsv)

def convert_csv(csvfilename):
    """Convert the original csv format to the new concise format"""
    oldobj = CsvFileOld(csvfilename)
    with TemporaryDirectory() as tmpdir:
        fcsvtmp = join(tmpdir, 'tmp.csv')
        assert not exists(fcsvtmp)
        newobj = CsvFileNew(fcsvtmp)
        with open(fcsvtmp, 'w', encoding='utf8') as ocsv:
            newobj.wr_hdrs(ocsv)
            for ntd in oldobj.get_ntdata():
                writer(ocsv, lineterminator='\n').writerow(ntd)
        assert exists(fcsvtmp)
        assert exists(csvfilename)
        rename(csvfilename, f'{csvfilename}.bac')
        assert not exists(csvfilename)
        assert exists(fcsvtmp)
        copy(fcsvtmp, csvfilename)
        assert exists(csvfilename)
        assert exists(fcsvtmp)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
