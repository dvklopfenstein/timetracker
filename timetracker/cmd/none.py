"""Do command, `none`"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from timetracker.cmd import common


def cli_run_none(fnamecfg, args):
    """Do command, `none`"""
    # pylint: disable=unused-argument
    cfg = common.get_cfg(fnamecfg)
    run_none(cfg.cfg_loc, args.name)

def run_none(cfg_proj, username=None):
    """If no Timetracker command is run, print informative messages"""
    # Check for start time
    if (startobj := cfg_proj.get_starttime_obj(username)) is not None:
        common.prtmsg_started01(startobj)
        return startobj
    # pylint: disable=import-outside-toplevel
    from timetracker.msgs import str_tostart
    print(str_tostart())
    return None


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
