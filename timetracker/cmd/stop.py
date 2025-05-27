"""Stop the timer and record this time unit"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from logging import error
from timetracker.cfg.utils import get_shortest_name
from timetracker.ntcsv import get_ntcsv
from timetracker.epoch.epoch import get_dtz
from timetracker.epoch.epoch import get_now
from timetracker.consts import FMTDT_H
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
    cfg = get_cfg(fnamecfg)
    return run_stop(cfg.cfg_loc, uname, csvfields, stop_at, **kwargs)

def run_stop(cfgproj, uname, csvfields, stop_at=None, **kwargs):
    """Stop the timer and record this time unit"""
    fcsv = cfgproj.get_filename_csv(uname, kwargs.get('dirhome'))
    # Get the elapsed time
    startobj = cfgproj.get_starttime_obj(uname)
    if startobj is None:
        return None
    dta = startobj.read_starttime()
    if dta is None:
        # pylint: disable=fixme
        # TODO: Check for local .timetracker/config file
        # TODO: Add project
        print('No elapsed time to stop; '
              'Do `trk start` to begin tracking time ')
              #f'for project, {cfgproj.project}')
        return {'fcsv':fcsv, 'csvline':None}
    now = get_now() if 'now' not in kwargs else kwargs['now']
    dtz = now if stop_at is None else get_dtz(stop_at, now, kwargs.get('defaultdt'))
    if dtz is None:
        raise RuntimeError(f'NO STOP TIME FOUND in "{stop_at}"; '
                           f'NOT STOPPING TIMER STARTED {dta.strftime(FMTDT_H)}')
    if dtz <= dta:
        error(f'NOT WRITING ELAPSED TIME: starttime({dta}) > stoptime({dtz})')
        return {'fcsv':fcsv, 'csvline':None}
    delta = dtz - dta

    # Append the timetracker file with this time unit
    if not fcsv:
        error('Not saving time interval; no csv filename was provided')
        return {'fcsv':fcsv, 'csvline':None}
    csvline = wr_stopline(fcsv, dta, delta, csvfields, dtz, kwargs.get('wr_old', False))
    _msg_stop_complete(fcsv, delta, dtz, kwargs.get('quiet', False))

    # Remove the starttime file
    if not kwargs.get('keepstart', False):
        startobj.rm_starttime()
    else:
        print('NOT restarting the timer because `--keepstart` invoked')
    return {'fcsv':fcsv, 'csvline':csvline}

def _msg_stop_complete(fcsv, delta, stoptime, quiet):
    """Finish stopping"""
    if not quiet:
        print('Timetracker stopped at: '
              f'{stoptime.strftime(FMTDT_H)}: '
              f'{stoptime}\n'
              f'Elapsed H:M:S {delta} '
              f'appended to {get_shortest_name(fcsv)}')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
