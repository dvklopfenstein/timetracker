"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from logging import debug
from timetracker.msgs import str_tostart
from timetracker.utils import yellow
from timetracker.cmd.common import get_cfg


def cli_run_none(fnamecfg, args):
    """noneialize timetracking on a project"""
    # pylint: disable=unused-argument
    run_none(fnamecfg, args.name)

def run_none(fnamecfg, name=None):
    """If no Timetracker command is run, print informative messages"""
    debug(yellow('RUNNING COMMAND NONE'))
    cfg = get_cfg(fnamecfg)
    # Check for start time
    cfglocal = cfg.cfg_loc
    ostart = cfglocal.get_starttime_obj(name)
    if ostart.file_exists():
        ostart.prtmsg_started01()
    else:
        print(str_tostart())


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
