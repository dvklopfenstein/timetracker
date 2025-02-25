"""Common messages"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"


def str_tostart():
    """Message instructing how to start the timer"""
    return 'Run `trk start` to start tracking'

def str_tostart_epoch():
    """Message instructing how to start the timer"""
    return ('Run `trk start --at time` to start tracking '
            'at a specific or elapsed time')

def str_how_to_stop_now():
    """Message to print when the timer is started"""
    return ('Run `trk stop -m "task description"` '
            'to stop tracking now and record this time unit')

def str_cancelled():
    """Message to print when the timer is canceled"""
    return 'Timer is canceled'

def str_not_running():
    """Message to print when the timer is canceled"""
    return 'Timer is not running'

def str_started_epoch():
    """Message to print when the timer is started"""
    return ('Run `trk stop -m "task description" --at time` '
            'to stop tracking at a specific or elapsed time')

def str_notrkrepo(trkdir):
    """Message when researcher is not in a dir or subdir that is managed by trk"""
    return f'fatal: not a Trk repository (or any of the parent directories): {trkdir}'

def str_init_empty_proj(cfglocal):
    """Message upon initializing an empyt timetracking project"""
    return f'Initialized empty Trk repository in {cfglocal.get_filename_cfg()}'

def str_init(dirproj):
    """Message that occurs when there is no Timetracking config file"""
    return ('Run `trk init` to initialize time-tracking '
           f'for the project in {dirproj}')

def str_notrkrepo_mount(mountname, trkdir):
    """Message when researcher is not in a dir or subdir that is managed by trk"""
    return f'fatal: not a Trk repository (or any parent up to mount point {mountname}): {trkdir}'


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
