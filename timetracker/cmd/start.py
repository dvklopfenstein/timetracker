"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from logging import debug

from datetime import datetime
from timetracker.utils import yellow
from timetracker.epoch.epoch import get_dtz
from timetracker.cmd.common import get_cfg


def cli_run_start(fnamecfg, args):
    """Initialize timetracking on a project"""
    _run_start(
        fnamecfg,
        args.name,
        start_at=args.at,
        force=args.force)
        ##activity=args.activity,

def _run_start(fnamecfg, name=None, start_at=None, **kwargs):
    """Initialize timetracking on a project"""
    debug(yellow('RUNNING COMMAND _START'))
    cfg = get_cfg(fnamecfg)
    cfgproj = cfg.cfg_loc
    return run_start(cfgproj, name, start_at, **kwargs)

def run_start(cfgproj, name=None, start_at=None, **kwargs):
    """Initialize timetracking on a project"""
    debug(yellow('RUNNING COMMAND START'))
    now = kwargs.get('now', datetime.now())
    start_obj = cfgproj.get_starttime_obj(name)
    if start_obj is None:
        return None

    # Print elapsed time, if timer was started
    if start_at is None:
        if start_obj.file_exists():
            start_obj.prtmsg_started01()
    else:
        start_obj.prt_elapsed()

    # Set (if not started) or reset (if start is forced) starting time
    force = kwargs.get('force', False)
    if not exists(start_obj.filename) or force:
        starttime = now if start_at is None else get_dtz(start_at, now, kwargs.get('defaultdt'))
        #assert isinstance(starttime, datetime), f'NOT A datetime: {starttime}'
        start_obj.wr_starttime(starttime, kwargs.get('activity'), kwargs.get('tag'))
        if not kwargs.get('quiet', False):
            print(f'Timetracker {_get_msg(start_at, force)}: '
                  f'{starttime.strftime("%a %I:%M %p")}: '
                  f'{starttime} ')
                  #f"for project '{cfgproj.project}'")

    # Informational message
    elif not force:
        if start_at is not None:
            print(f'Run `trk start --at {start_at} --force` to force restart')
    return start_obj

def _get_msg(start_at, force):
    if force:
        return "reset to"
    return "started now" if start_at is None else "started at"


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
