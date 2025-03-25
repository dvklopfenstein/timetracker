"""Utilities for configuration parser"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from csv import reader


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


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
