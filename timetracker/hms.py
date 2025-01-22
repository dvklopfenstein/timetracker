"""Format date"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from datatime import timedelta
from timeit import default_timer


# 2025-01-21 17:09:47.035936
FMT = '%y-%m-%d %H:%M:%S.%f'


def str_hms_dts(dt0, dt1):
    pass

def str_hms_tic(tic):
    return str(timedelta(seconds=default_timer()-tic))
    

# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
