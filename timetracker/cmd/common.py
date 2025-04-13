"""Functions used by multiple commands"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists

from timetracker.msgs import str_uninitialized
from timetracker.cfg.cfg import Cfg


def get_cfg(fnamecfg):
    """Get the Cfg object, exit if no CfgProj exists"""
    if str_uninitialized(fnamecfg):
        sys_exit(0)
    return Cfg(fnamecfg)

def get_fcsv(cfg_proj, uname, dirhome=None):
    """Get the name of the csv file, if it exists"""
    if exists(cfg_proj.filename):
        fcsv = cfg_proj.get_filename_csv(uname, dirhome)
        if not exists(fcsv):
            _no_csv(fcsv, cfg_proj, uname)
            return None
        return fcsv
    return None

def _no_csv(fcsv, cfgproj, uname):
    start_obj = cfgproj.get_starttime_obj(uname)
    start_obj.prtmsg_started_csv(fcsv)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
