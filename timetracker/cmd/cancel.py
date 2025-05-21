"""Cancel a timer if it is started"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from timetracker.msgs import str_cancelled1
from timetracker.msgs import str_not_running
from timetracker.cmd.common import prt_elapsed
from timetracker.cfg.cfg_local import CfgProj


def cli_run_cancel(fnamecfg, args):
    """Cancel a timer if it is started"""
    run_cancel(
        CfgProj(fnamecfg),
        args.name)

def run_cancel(cfgproj, name=None):
    """Cancel a timer if it is started"""
    if (startobj := cfgproj.get_starttime_obj(name)) and startobj.started():
        prt_elapsed(startobj, f'{str_cancelled1()}; was')
        startobj.rm_starttime()
        return startobj.filename
    print(str_not_running())
    return None


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
