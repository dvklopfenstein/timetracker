"""Functions used by multiple commands"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists

from timetracker.msgs import str_uninitialized
from timetracker.cfg.cfg_local  import CfgProj


def get_fcsv(fnamecfg, uname, dirhome=None):
    """Get the name of the csv file, if it exists"""
    if str_uninitialized(fnamecfg):
        sys_exit(0)
    cfgproj = CfgProj(fnamecfg, dirhome=dirhome)
    fcsv = cfgproj.get_filename_csv(uname)
    if not exists(fcsv):
        _no_csv(fcsv, cfgproj, uname)
        return None
    return fcsv

def _no_csv(fcsv, cfgproj, uname):
    start_obj = cfgproj.get_starttime_obj(uname)
    start_obj.prtmsg_started_csv(fcsv)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
