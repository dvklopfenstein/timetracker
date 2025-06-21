"""Functions used by multiple commands"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from timetracker.msgs import str_tostart
from timetracker.consts import FMTDT_H


def get_cfg(fnamecfg):
    """Get the Cfg object, exit if no CfgProj exists"""
    # pylint: disable=import-outside-toplevel
    if str_uninitialized(fnamecfg):
        from sys import exit as sys_exit
        sys_exit(0)
    from timetracker.cfg.cfg import Cfg
    return Cfg(fnamecfg)

def str_uninitialized(fcfgloc):
    """Print an init message if the timetracker local configuration does not exist"""
    # pylint: disable=import-outside-toplevel
    import os.path as os_path
    if os_path.exists(fcfgloc):
        return False
    from timetracker.utils import yellow
    from timetracker.msgs import str_init
    print(yellow(str_init(os_path.dirname(os_path.dirname(fcfgloc)))))
    return True

def no_csv(fcsv, cfgproj, uname):
    """Messages to print if there is no csv file"""
    # pylint: disable=import-outside-toplevel
    from timetracker.msgs import str_no_time_recorded
    print(str_no_time_recorded(fcsv))
    if (startobj := cfgproj.get_starttime_obj(uname)):
        prtmsg_started01(startobj)
    else:
        print(str_tostart())

def add_tag_billable(args):
    """Add a 'Billable' tag to the tags list"""
    if args.tags is None:
        args.tags = ['Billable']
    else:
        args.tags.append('Billable')

# ---------------------------------------------------------
def prtmsg_started01(startobj):
    """Print message depending if timer is started or not"""
    if (dtstart := startobj.read_starttime()):
        prtmsg_start_01(startobj, dtstart)
    else:
        print(str_tostart())

def prtmsg_start_01(startobj, dtstart, force=False):
    """Print message depending if timer is started or not; no starting instructions"""
    hms = startobj.hms_from_startfile(dtstart)
    hms1 = hms is not None
    # pylint: disable=import-outside-toplevel
    if hms1 and hms <= startobj.min_trigger:
        _prtmsg_basic(startobj, dtstart, hms, force)
    elif hms1:
        _prtmsg_triggered(startobj, dtstart, hms, force)
    else:
        from timetracker.utils import prt_todo
        prt_todo('TODO: STARTFILE WITH NO HMS')

def _prtmsg_triggered(startobj, dta, hms, force):
    """Print message info regarding triggered (started) timer"""
    # pylint: disable=import-outside-toplevel
    from timetracker.epoch.epoch import str_arg_epoch
    from timetracker.msgs import str_started_epoch
    from timetracker.msgs import str_tostart_epoch
    _prt_started_n_running(startobj, dta, hms)
    print(str_started_epoch())
    print(str_arg_epoch(dta, desc=' after start'))
    _prtmsg_basic(startobj, dta, hms, force)
    print(str_started_epoch())
    print(str_tostart_epoch())

def _prtmsg_basic(startobj, dta, hms, force):
    """Print basic start time message"""
    _prt_started_n_running(startobj, dta, hms)
    if not force:
        # pylint: disable=import-outside-toplevel
        from timetracker.msgs import str_how_to_stop_now
        print(str_how_to_stop_now())

def _prt_started_n_running(startobj, dta, hms):
    """Return a string detailing how long the timer has been running"""
    msg = startobj.str_elapsed_hms(
          hms,
          f'Timer started on {dta.strftime(FMTDT_H)} and running')
    print(msg)

# ---------------------------------------------------------
def prt_elapsed(startobj, pretxt='Timer running;'):
    """Print elapsed time if timer is started"""
    # pylint: disable=import-outside-toplevel
    if (dtstart := startobj.read_starttime()) is not None:
        if (hms := startobj.hms_from_startfile(dtstart)) is not None:
            msg = f'{pretxt} started {dtstart.strftime(FMTDT_H)}; running'
            print(startobj.str_elapsed_hms(hms, msg))
        else:
            from timetracker.msgs import str_not_running
            print(str_not_running())


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
