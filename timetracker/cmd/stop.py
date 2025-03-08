"""Stop the timer and record this time unit"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
from logging import debug
from logging import error
from datetime import datetime
from timetracker.cfg.cfg_local  import CfgProj
from timetracker.cfg.utils import get_shortest_name
from timetracker.csvold import CsvFile
from timetracker.consts import FMTDT_H
from timetracker.msgs import str_uninitialized
from timetracker.ntcsv import get_ntcsv
from timetracker.epoch import get_dtz
from timetracker.utils import yellow


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
    debug(yellow('RUNNING COMMAND STOP'))
    if str_uninitialized(fnamecfg):
        sys_exit(0)
    cfgproj = CfgProj(fnamecfg, dirhome=kwargs.get('dirhome'))
    fcsv = cfgproj.get_filename_csv(uname)
    # Get the elapsed time
    start_obj = cfgproj.get_starttime_obj(uname)
    dta = start_obj.read_starttime()
    if dta is None:
        # pylint: disable=fixme
        # TODO: Check for local .timetracker/config file
        # TODO: Add project
        print('No elapsed time to stop; '
              'Do `trk start` to begin tracking time '
              f'for project, {cfgproj.project}')
        return {'fcsv':fcsv, 'csvline':None}
    stopat = kwargs.get('stop_at')
    now = kwargs.get('now', datetime.now())
    dtz = now if stopat is None else get_dtz(stopat, now, kwargs.get('defaultdt', now))
    if dtz <= dta:
        error(f'NOT WRITING ELAPSED TIME: starttime({dta}) > stoptime({dtz})')
        return {'fcsv':fcsv, 'csvline':None}
    delta = dtz - dta

    # Append the timetracker file with this time unit
    debug(yellow(f'STOP: CSVFILE   exists({int(exists(fcsv))}) {fcsv}'))
    if not fcsv:
        error('Not saving time interval; no csv filename was provided')
        return {'fcsv':fcsv, 'csvline':None}
    csvline = CsvFile(fcsv).wr_stopline(dta, dtz, delta, csvfields)
    _msg_stop_complete(fcsv, delta, dtz, kwargs.get('quiet', False))

    # Remove the starttime file
    if not kwargs.get('keepstart', False):
        start_obj.rm_starttime()
    else:
        print('NOT restarting the timer because `--keepstart` invoked')
    return {'fcsv':fcsv, 'csvline':csvline}

def _msg_stop_complete(fcsv, delta, dtz, quiet):
    """Finish stopping"""
    debug(yellow(f'STOP: CSVFILE   exists({int(exists(fcsv))}) {fcsv}'))
    if not quiet:
        print(f'Timer stopped at {dtz.strftime(FMTDT_H)}\n'
              f'Elapsed H:M:S {delta} '
              f'appended to {get_shortest_name(fcsv)}')



####def _wr_csv_hdrs(fcsv):
####    # aTimeLogger columns: Activity From To Notes
####    with open(fcsv, 'w', encoding='utf8') as prt:
####        print(
####            'startsecs,'
####            'stopsecs,'
####            # Info
####            'message,',
####            'activity,',
####            'tags',
####            file=prt,
####        )


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
