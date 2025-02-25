"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os import remove
from os.path import exists
from os.path import dirname
from logging import debug

from timetracker.msgs import str_cancelled
from timetracker.msgs import str_init
from timetracker.utils import yellow
from timetracker.cfg.cfg_local  import CfgProj


def cli_run_cancel(fnamecfg, args):
    """Initialize timetracking on a project"""
    run_cancel(
        fnamecfg,
        args.name)

def run_cancel(fnamecfg, name=None):
    """Initialize timetracking on a project"""
    debug(yellow('START: RUNNING COMMAND CANCEL'))
    if not exists(fnamecfg):
        print(str_init(dirname(fnamecfg)))
        sys_exit(0)
    cfgproj = CfgProj(fnamecfg)
    start_obj = cfgproj.get_starttime_obj(name)
    fin_start = start_obj.filename
    if exists(fin_start):
        start_obj.prt_elapsed()
        remove(fin_start)
        print(str_cancelled())
    else:
        pass
    return fin_start


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
