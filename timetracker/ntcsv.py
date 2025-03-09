"""Functions used by multiple commands"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from collections import namedtuple


NTTIMEDATA = namedtuple('TimeData', 'start_datetime duration message activity tags')

NTCSV = namedtuple("CsvFields", "message activity tags")

def get_ntcsv(message, activity='', tags=None):
    """Get a namedtuple with csv row info: message, activity, & tags"""
    return NTCSV(
        message=message,
        activity=activity if activity is not None else '',
        tags=';'.join(tags) if tags is not None else '')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
