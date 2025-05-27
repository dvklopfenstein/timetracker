"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from timetracker.epoch.epoch import get_dtz
from timetracker.epoch.epoch import get_now
from timetracker.cmd.common import get_cfg
from timetracker.cmd.common import prtmsg_start_01
from timetracker.cmd.common import prt_elapsed


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
    cfg = get_cfg(fnamecfg)
    cfgproj = cfg.cfg_loc
    return run_start(cfgproj, name, start_at, **kwargs)

def run_start(cfgproj, name=None, start_at=None, **kwargs):
    """Initialize timetracking on a project"""
    now = get_now() if 'now' not in kwargs else kwargs['now']
    startobj = cfgproj.get_starttime_obj(name)
    if startobj is None:
        return None

    # Print elapsed time, if timer was started
    force = kwargs.get('force', False)
    if start_at is None:
        if (dtstart := startobj.read_starttime()):
            prtmsg_start_01(startobj, dtstart, force)
    else:
        prt_elapsed(startobj)

    # Set (if not started) or reset (if start is forced) starting time
    if not startobj.started() or force:
        starttime = now if start_at is None else get_dtz(start_at, now, kwargs.get('defaultdt'))
        if starttime is None:
            return startobj
        startobj.wr_starttime(starttime, kwargs.get('activity'), kwargs.get('tag'))
        if not kwargs.get('quiet', False):
            print(f'Timetracker {_get_msg(start_at, force)}: '
                  f'{starttime.strftime("%a %I:%M %p")}: '
                  f'{starttime} ')
                  #f"for project '{cfgproj.project}'")

    # Informational message
    elif not force:
        if start_at is not None:
            print(f'Run `trk start --at {start_at} --force` to force restart')
    return startobj

def _get_msg(start_at, force):
    if force:
        return "start reset to"
    return "started now" if start_at is None else "started at"


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
