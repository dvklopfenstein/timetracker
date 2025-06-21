"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from timetracker.epoch.epoch import get_dt_at
from timetracker.cmd import common


def cli_run_start(fnamecfg, args):
    """Initialize timetracking on a project"""
    _run_start(
        fnamecfg,
        args.name,
        start_at=args.at,
        force=args.force)

def _run_start(fnamecfg, name=None, start_at=None, **kwargs):
    """Initialize timetracking on a project"""
    cfg = common.get_cfg(fnamecfg)
    cfgproj = cfg.cfg_loc
    return run_start(cfgproj, name, start_at, **kwargs)

def run_start(cfgproj, name=None, start_at=None, **kwargs):
    """Initialize timetracking on a project"""
    startobj = cfgproj.get_starttime_obj(name)
    if startobj is None:
        return None

    # Print elapsed time, if timer was started
    force = kwargs.get('force', False)
    if start_at is None:
        if (dtstart := startobj.read_starttime()):
            common.prtmsg_start_01(startobj, dtstart, force)
    else:
        common.prt_elapsed(startobj)

    # Set (if not started) or reset (if start is forced) starting time
    if not startobj.started() or force:
        starttime = get_dt_at(start_at, kwargs.get('now'), kwargs.get('defaultdt'))
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
