"""Stop the timer and record this time unit"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from logging import debug
from logging import error
from datetime import datetime
from timetracker.cfg.utils import get_shortest_name
from timetracker.ntcsv import get_ntcsv
from timetracker.epoch.epoch import get_dtz
from timetracker.consts import FMTDT_H
from timetracker.utils import yellow
from timetracker.csvrun import wr_stopline
from timetracker.cmd.common import get_cfg


def cli_run_stop(fnamecfg, args):
    """Stop the timer and record this time unit"""
    _run_stop(
        fnamecfg,
        args.name,
        get_ntcsv(args.message, args.activity, args.tags),
        keepstart=args.keepstart,
        stop_at=args.at)

def _run_stop(fnamecfg, uname, csvfields, stop_at=None, **kwargs):
    """Stop the timer and record this time unit"""
    # Get the starting time, if the timer is running
    debug(yellow('RUNNING COMMAND _STOP'))
    cfg = get_cfg(fnamecfg)
    cfgproj = cfg.cfg_loc
    return run_stop(cfgproj, uname, csvfields, stop_at, **kwargs)

def run_stop(cfgproj, uname, csvfields, stop_at=None, **kwargs):
    """Stop the timer and record this time unit"""
    debug(yellow('RUNNING COMMAND STOP'))
    fcsv = cfgproj.get_filename_csv(uname, kwargs.get('dirhome'))
    # Get the elapsed time
    start_obj = cfgproj.get_starttime_obj(uname)
    if start_obj is None:
        return None
    dta = start_obj.read_starttime()
    if dta is None:
        # pylint: disable=fixme
        # TODO: Check for local .timetracker/config file
        # TODO: Add project
        print('No elapsed time to stop; '
              'Do `trk start` to begin tracking time ')
              #f'for project, {cfgproj.project}')
        return {'fcsv':fcsv, 'csvline':None}
    now = kwargs.get('now', datetime.now())
    dtz = now if stop_at is None else get_dtz(stop_at, now, kwargs.get('defaultdt'))
    #print('DTZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ', dtz, uname, fcsv)
    if dtz is None:
        raise RuntimeError(f'NO STOP TIME FOUND in "{stop_at}"; '
                           f'NOT STOPPING TIMER STARTED {dta.strftime(FMTDT_H)}')
    if dtz <= dta:
        error(f'NOT WRITING ELAPSED TIME: starttime({dta}) > stoptime({dtz})')
        return {'fcsv':fcsv, 'csvline':None}
    delta = dtz - dta

    # Append the timetracker file with this time unit
    debug(yellow(f'STOP: CSVFILE   exists({int(exists(fcsv))}) {fcsv}'))
    if not fcsv:
        error('Not saving time interval; no csv filename was provided')
        return {'fcsv':fcsv, 'csvline':None}
    csvline = wr_stopline(fcsv, dta, delta, csvfields, dtz, kwargs.get('wr_old', False))
    ##csvline = CsvFile(fcsv).wr_stopline(dta, dtz, delta, csvfields)
    _msg_stop_complete(fcsv, delta, dtz, kwargs.get('quiet', False))

    # Remove the starttime file
    if not kwargs.get('keepstart', False):
        start_obj.rm_starttime()
    else:
        print('NOT restarting the timer because `--keepstart` invoked')
    return {'fcsv':fcsv, 'csvline':csvline}

def _msg_stop_complete(fcsv, delta, stoptime, quiet):
    """Finish stopping"""
    debug(yellow(f'STOP: CSVFILE   exists({int(exists(fcsv))}) {fcsv}'))
    if not quiet:
        print('Timetracker stopped at: '
              f'{stoptime.strftime(FMTDT_H)}: '
              f'{stoptime}\n'
              f'Elapsed H:M:S {delta} '
              f'appended to {get_shortest_name(fcsv)}')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
