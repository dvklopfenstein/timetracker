"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from timetracker.msgs import str_uninitialized
from timetracker.msgs import str_tostart
from timetracker.cfg.cfg_local import CfgProj


def cli_run_none(fnamecfg, args):
    """noneialize timetracking on a project"""
    # pylint: disable=unused-argument
    run_none(fnamecfg, args.name)

def run_none(fnamecfg, name=None):
    """If no Timetracker command is run, print informative messages"""
    if str_uninitialized(fnamecfg):
        sys_exit(0)
    # Check for start time
    cfglocal = CfgProj(fnamecfg)
    ostart = cfglocal.get_starttime_obj(name)
    if ostart.file_exists():
        ostart.prtmsg_started01()
    else:
        print(str_tostart())


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
