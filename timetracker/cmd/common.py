"""Functions used by multiple commands"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit

from timetracker.utils import prt_todo
from timetracker.msgs import str_uninitialized
from timetracker.msgs import str_tostart
from timetracker.msgs import str_no_time_recorded
from timetracker.msgs import str_started_epoch
from timetracker.msgs import str_tostart_epoch
from timetracker.msgs import str_how_to_stop_now
from timetracker.cfg.cfg import Cfg
from timetracker.epoch.epoch import str_arg_epoch
from timetracker.consts import FMTDT_H
from timetracker.msgs import str_not_running


def get_cfg(fnamecfg):
    """Get the Cfg object, exit if no CfgProj exists"""
    if str_uninitialized(fnamecfg):
        sys_exit(0)
    return Cfg(fnamecfg)

def no_csv(fcsv, cfgproj, uname):
    """Messages to print if there is no csv file"""
    startobj = cfgproj.get_starttime_obj(uname)
    print(str_no_time_recorded(fcsv))
    if startobj:
        prtmsg_started01(startobj)
    else:
        print(str_tostart())

# ---------------------------------------------------------
def prtmsg_started01(startobj):
    """Print message depending if timer is started or not"""
    dtstart = startobj.read_starttime()
    if dtstart:
        _prtmsg_started01(startobj, dtstart)

def _prtmsg_started01(startobj, dtstart):
    hms = startobj.hms_from_startfile(dtstart)
    hms1 = hms is not None
    if hms1 and hms <= startobj.min_trigger:
        _prtmsg_basic(startobj, dtstart, hms)
    elif hms1:
        _prtmsg_triggered(startobj, dtstart, hms)
    else:
        prt_todo('TODO: STARTFILE WITH NO HMS')

def _prtmsg_triggered(startobj, dta, hms):
    """Print message info regarding triggered (started) timer"""
    startobj.str_started_n_running(dta, hms)
    print(str_started_epoch())
    print(str_arg_epoch(dta, desc=' after start'))
    _prtmsg_basic(startobj, dta, hms)
    print(str_started_epoch())
    print(str_tostart_epoch())

def _prtmsg_basic(startobj, dta, hms):
    """Print basic start time message"""
    startobj.str_started_n_running(dta, hms)
    print(str_how_to_stop_now())

# ---------------------------------------------------------
def prt_elapsed(startobj, msg='Timer running;'):
    """Print elapsed time if timer is started"""
    # Print elapsed time, if timer was started
    dtstart = startobj.read_starttime()
    if dtstart is not None:
        hms = startobj.hms_from_startfile(dtstart)
        # pylint: disable=line-too-long
        return _prt_startdt_n_elapsed(startobj, dtstart, hms, msg) if hms is not None else str_not_running()
    return None

def _prt_startdt_n_elapsed(startobj, startdt, hms, msg):
    msg = f'{msg} started {startdt.strftime(FMTDT_H)}; running'
    print(startobj.str_elapsed_hms(hms, msg))


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
