"""Utilities for configuration parser"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from datetime import datetime
from datetime import timedelta
from csv import reader
from timetracker.consts import FMTDT
from timetracker.consts import FMTDT24HMS

STRPTIME = datetime.strptime


def get_hdr(csvfilename):
    """Get the header in the csv file"""
    with open(csvfilename, encoding='utf8') as csvstrm:
        hdrs, _ = get_hdr_itr(csvstrm)
        return hdrs

def get_hdr_itr(istream):
    """Get a header and an iterator from a input file stream"""
    timereader = reader(istream)
    itr = iter(timereader)
    hdr = next(itr)
    return hdr, itr

# --------------------------------------------------------------
def dt_from_str(txt):
    """Get a datetime object, given a string"""
    return STRPTIME(txt, FMTDT) if len(txt) > 19 else STRPTIME(txt, FMTDT24HMS)

def td_from_str(txt):
    """Get a timedelta, given a string"""
    slen = len(txt)
    if (slen in {14, 15} and txt[-7] == '.') or slen in {7, 8}:
        return _td_from_hms(txt, slen)
    daystr, hms = txt.split(',')
    return _td_from_hms(hms[1:], len(hms)-1) + \
           timedelta(days=int(daystr.split(maxsplit=1)[0]))

def _td_from_hms(txt, slen):
    """Get a timedelta, given 8:00:00 or 12:00:01.100001"""
    if slen in {14, 15} and txt[-7] == '.':
        dto = STRPTIME(txt, "%H:%M:%S.%f")
        return timedelta(hours=dto.hour,
                         minutes=dto.minute,
                         seconds=dto.second,
                         microseconds=dto.microsecond)
    assert slen in {7, 8}
    dto = STRPTIME(txt, "%H:%M:%S")
    return timedelta(hours=dto.hour, minutes=dto.minute, seconds=dto.second)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
