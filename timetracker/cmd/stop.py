"""Stop the timer and record this time unit"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
#from os.path import relpath
from os.path import dirname
#from logging import info
from logging import debug
from logging import error
from collections import namedtuple
from datetime import datetime
##from timeit import default_timer
from timetracker.utils import yellow
from timetracker.epoch import get_dtz
from timetracker.cfg.cfg_local  import CfgProj
from timetracker.cfg.utils import get_shortest_name
from timetracker.msgs import str_init


NTCSV = namedtuple("CsvFields", "message activity tags")

def get_ntcsv(message, activity=None, tags=None):
    """Get a namedtuple with csv row information"""
    return NTCSV(
        message=message,
        activity=activity if activity is not None else '',
        tags=';'.join(tags) if tags is not None else '')

def cli_run_stop(fnamecfg, args):
    """Stop the timer and record this time unit"""
    run_stop(
        fnamecfg,
        args.name,
        get_ntcsv(args.message, args.activity, args.tags),
        quiet=args.quiet,
        keepstart=args.keepstart,
        stop_at=args.at)

#def run_stop(fnamecfg, csvfields, quiet=False, keepstart=False):
def run_stop(fnamecfg, uname, csvfields, **kwargs):
    """Stop the timer and record this time unit"""
    # Get the starting time, if the timer is running
    debug(yellow('STOP: RUNNING COMMAND STOP'))
    if not exists(fnamecfg):
        print(str_init(dirname(fnamecfg)))
        sys_exit(0)
        #sys_exit(str_init(dirname(fnamecfg)))
    cfgproj = CfgProj(fnamecfg, dirhome=kwargs.get('dirhome'))
    # Get the elapsed time
    start_obj = cfgproj.get_starttime_obj(uname)
    dta = start_obj.read_starttime()
    dtz = _get_dtz(kwargs.get('stop_at'), dta)
    if dta is None:
        # pylint: disable=fixme
        # TODO: Check for local .timetracker/config file
        # TODO: Add project
        error('NOT WRITING ELAPSED TIME; '
              'Do `trk start` to begin tracking time '
              'for project, TODO')
        return None
    if dtz <= dta:
        error('NOT WRITING ELAPSED TIME: '
              f'starttime({dta}) > stoptime({dtz})')
        return None

    # Append the timetracker file with this time unit
    fcsv = cfgproj.get_filename_csv(uname)
    debug(yellow(f'STOP: CSVFILE   exists({int(exists(fcsv))}) {fcsv}'))
    if not fcsv:
        error('Not saving time interval; no csv filename was provided')
    ####_msg_csv(fcsv)
    # Print header into csv, if needed
    if not exists(fcsv):
        _wr_csvlong_hdrs(fcsv)
    # Print time information into csv
    delta = dtz - dta
    csvline = _strcsv_timerstopped(
        dta, dtz, delta,
        csvfields.message,
        csvfields.activity,
        csvfields.tags)
    _wr_csvlong_data(fcsv, csvline)

    debug(yellow(f'STOP: CSVFILE   exists({int(exists(fcsv))}) {fcsv}'))
    if not kwargs.get('quiet', False):
        print(f'Timer stopped; Elapsed H:M:S={delta} '
              f'appended to {get_shortest_name(fcsv)}')
    # Remove the starttime file
    if not kwargs.get('keepstart', False):
        start_obj.rm_starttime()
    else:
        print('NOT restarting the timer because `--keepstart` invoked')
    return fcsv

def _get_dtz(timetxt, dta):
    return datetime.now() if not timetxt else get_dtz(timetxt, dta)


####def _msg_csv(fcsv):
####    if fcsv:
####        debug(f'STOP: CSVFILE   exists({int(exists(fcsv))}) {fcsv}')
####    else:
####        error('Not saving time interval; no csv filename was provided')

def _wr_csvlong_hdrs(fcsv):
    # aTimeLogger columns: Activity From To Notes
    with open(fcsv, 'w', encoding='utf8') as prt:
        print(
            'start_day,'
            'xm,'
            'start_datetime,'
            # Stop
            'stop_day,'
            'zm,'
            'stop_datetime,'
            # Duration
            'duration,'
            # Info
            'message,'
            'activity,'
            'tags',
            file=prt,
        )

def _wr_csvlong_data(fcsv, csvline):
    with open(fcsv, 'a', encoding='utf8') as ostrm:
        print(csvline, file=ostrm)

def _strcsv_timerstopped(dta, dtz, delta, message, activity, tags):
    # pylint: disable=unknown-option-value,too-many-arguments, too-many-positional-arguments
    return (f'{dta.strftime("%a")},{dta.strftime("%p")},{dta},'
            f'{dtz.strftime("%a")},{dtz.strftime("%p")},{dtz},'
            f'{delta},'
            f'{message},'
            f'{activity},'
            f'{tags}')


def _wr_csv_hdrs(fcsv):
    # aTimeLogger columns: Activity From To Notes
    with open(fcsv, 'w', encoding='utf8') as prt:
        print(
            'startsecs,'
            'stopsecs,'
            # Info
            'message,',
            'activity,',
            'tags',
            file=prt,
        )


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
