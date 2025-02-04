"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
from timetracker.msgs import str_started
from timetracker.msgs import str_init
from timetracker.cfg.cfg_local import CfgProj


def cli_run_none(fcfgproj, args):
    """noneialize timetracking on a project"""
    # pylint: disable=unused-argument
    run_none(fcfgproj)

def run_none(fcfgproj):
    """If no Timetracker command is run, print informative messages"""
    if not exists(fcfgproj):
        print(str_init())
        sys_exit()
    # Check for start time
    cfglocal = CfgProj(fcfgproj)
    start_file = cfglocal.get_filename_start()
    if not exists(start_file):
        print('Run `trk start` to begin timetracking')
    else:
        cfglocal.prt_elapsed()
        print(str_started())


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
