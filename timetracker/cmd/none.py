"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
from os.path import dirname
from timetracker.msgs import str_init
from timetracker.cfg.cfg_local import CfgProj


def cli_run_none(fcfgproj, args):
    """noneialize timetracking on a project"""
    # pylint: disable=unused-argument
    run_none(fcfgproj, args.name)

def run_none(fcfgproj, name=None):
    """If no Timetracker command is run, print informative messages"""
    if not exists(fcfgproj):
        print(str_init(dirname(fcfgproj)))
        sys_exit(0)
    # Check for start time
    cfglocal = CfgProj(fcfgproj)
    cfglocal.get_starttime_obj(name).prtmsg_started01()


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
