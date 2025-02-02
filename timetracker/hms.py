"""Format date"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

##from datetime import timedelta
from os.path import exists
from datetime import datetime
##from timeit import default_timer


# 2025-01-21 17:09:47.035936
FMT = '%Y-%m-%d %H:%M:%S.%f'


def hms_from_startfile(fname):
    """Get the elapsed time starting from time in a starttime file"""
    dtstart = read_starttime(fname)
    return datetime.now() - dtstart if dtstart is not None else None

##def str_hms_dts(dt0, dt1):
##    pass
##
##def str_hms_tic(tic):
##    return str(timedelta(seconds=default_timer()-tic))

def read_starttime(fname):
    """Get datetime from a starttime file"""
    if exists(fname):
        with open(fname, encoding='utf8') as ifstrm:
            for line in ifstrm:
                line = line.strip()
                assert len(line) == 26  # "2025-01-22 04:05:00.086891"
                return datetime.strptime(line, FMT)
    return None



# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
