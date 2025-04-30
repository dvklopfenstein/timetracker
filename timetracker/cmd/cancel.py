"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import remove
from os.path import exists
from logging import debug

from timetracker.msgs import str_cancelled1
from timetracker.msgs import str_not_running
from timetracker.utils import yellow
from timetracker.cfg.cfg_local import CfgProj


def cli_run_cancel(fnamecfg, args):
    """Initialize timetracking on a project"""
    run_cancel(
        CfgProj(fnamecfg),
        args.name)

def run_cancel(cfgproj, name=None):
    """Initialize timetracking on a project"""
    debug(yellow('RUNNING COMMAND CANCEL'))
    start_obj = cfgproj.get_starttime_obj(name)
    if start_obj and exists(start_obj.filename):
        start_obj.prt_elapsed(f'{str_cancelled1()}; was')
        remove(start_obj.filename)
        return start_obj.filename
    print(str_not_running())
    return None


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
