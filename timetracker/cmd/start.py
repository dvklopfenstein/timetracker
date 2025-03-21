"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
from logging import debug

from datetime import datetime
from timetracker.msgs import str_uninitialized
from timetracker.utils import yellow
from timetracker.epoch.epoch import get_dtz
from timetracker.cfg.cfg_local  import CfgProj


def cli_run_start(fnamecfg, args):
    """Initialize timetracking on a project"""
    run_start(
        fnamecfg,
        args.name,
        start_at=args.at,
        force=args.force,
        ##activity=args.activity,
        quiet=args.quiet)

def run_start(fnamecfg, name=None, **kwargs):
    """Initialize timetracking on a project"""
    debug(yellow('RUNNING COMMAND START'))
    now = kwargs.get('now', datetime.now())
    if str_uninitialized(fnamecfg):
        sys_exit(0)
    cfgproj = CfgProj(fnamecfg)
    start_obj = cfgproj.get_starttime_obj(name)

    # Print elapsed time, if timer was started
    start_at = kwargs.get('start_at')
    if start_at is None:
        if start_obj.file_exists():
            start_obj.prtmsg_started01()
    else:
        start_obj.prt_elapsed()

    # Set (if not started) or reset (if start is forced) starting time
    force = kwargs.get('force', False)
    if not exists(start_obj.filename) or force:
        #cfg_global = CfgGlobal(dirhome)
        #chgd = cfg_global.add_proj(cfgproj.project, cfgproj.get_filename_cfgproj())
        #if chgd:
        #    cfg_global.wr_cfg()
        starttime = now if start_at is None else get_dtz(start_at, now, kwargs.get('defaultdt'))
        #assert isinstance(starttime, datetime), f'NOT A datetime: {starttime}'
        start_obj.wr_starttime(starttime, kwargs.get('activity'), kwargs.get('tag'))
        if not kwargs.get('quiet', False):
            print(f'Timetracker {_get_msg(start_at, force)}: '
                  f'{starttime.strftime("%a %I:%M %p")}: {starttime} '
                  f"for project '{cfgproj.project}'")

    # Informational message
    elif not force:
        ## if start_at is None:
        ##     print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAaa')
        ##     print(str_how_to_stop_now())
        ## else:
        if start_at is not None:
            print(f'Run `trk start --at {start_at} --force` to force restart')
    return start_obj.filename

def _get_msg(start_at, force):
    if force:
        return "reset to"
    return "started now" if start_at is None else "started at"


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
