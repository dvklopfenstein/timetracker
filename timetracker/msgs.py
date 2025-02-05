"""Common messages"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import getcwd


def str_started():
    """Message to print when the timer is started"""
    return 'Do `trk stop -m "task description"` to stop tracking this time unit'
    ##Test feature
    ##print('    Do `trk start --force`              to reset start time to now')

def str_notrkrepo(trkdir):
    """Message when researcher is not in a dir or subdir that is managed by trk"""
    return f'fatal: not a Trk repository (or any of the parent directories): {trkdir}'

def str_init_empty_proj(cfglocal):
    """Message upon initializing an empyt timetracking project"""
    return f'Initialized empty Trk repository in {cfglocal.get_filename_cfglocal()}'

def str_init():
    """Message that occurs when there is no Timetracking config file"""
    return ('Run `trk init` to initialize time-tracking '
           f'for the project in {getcwd()}')

def str_notrkrepo_mount(mountname, trkdir):
    """Message when researcher is not in a dir or subdir that is managed by trk"""
    return f'fatal: not a Trk repository (or any parent up to mount point {mountname}): {trkdir}'


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
