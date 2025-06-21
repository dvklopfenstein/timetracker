"""Cancel a timer if it is started"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from timetracker import msgs
from timetracker.cmd import common
from timetracker.cfg.cfg_local import CfgProj


def cli_run_cancel(fnamecfg, args):
    """Cancel a timer if it is started"""
    run_cancel(
        CfgProj(fnamecfg),
        args.name)

def run_cancel(cfgproj, name=None):
    """Cancel a timer if it is started"""
    if (startobj := cfgproj.get_starttime_obj(name)) and startobj.started():
        common.prt_elapsed(startobj, f'{msgs.str_cancelled1()}; was')
        startobj.rm_starttime()
        return startobj.filename
    print(msgs.str_not_running())
    return None


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
