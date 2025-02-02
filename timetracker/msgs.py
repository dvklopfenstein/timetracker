"""Common messages"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"


def str_started():
    """Message to print when the timer is started"""
    return 'Do `trk stop -m "task description"` to stop tracking this time unit'
    ##Test feature
    ##print('    Do `trk start --force`              to reset start time to now')

def str_notrkrepo(trkdir):
    """Message when researcher is not in a dir or subdir that is managed by trk"""
    return f'fatal: not a trk repository (or any of the parent directories): {trkdir}'

def str_notrkrepo_mount(mountname, trkdir):
    """Message when researcher is not in a dir or subdir that is managed by trk"""
    return f'fatal: not a trk repository (or any parent up to mount point {mountname}): {trkdir}'


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
