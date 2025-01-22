"""Stop the timer and record this time unit"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from logging import error
from datetime import datetime
from timetracker.hms import read_startfile


def run_stop(fmgr):
    """Stop the timer and record this time unit"""
    # Get the starting time, if the timer is running
    dta = read_startfile(fmgr.get_filename_start())
    if dta is None:
        error('NOT WRITING ELAPSED TIME; NO STARTING TIME FOUND')
        return

    # Append the timetracker file with this time unit
    fcsv = fmgr.get_filename_csv()
    if not exists(fcsv):
        _wr_csvhdrs(fcsv)
    with open(fcsv, 'a', encoding='utf8') as ostrm:
        dtz = datetime.now()
        delta = dtz - dta
        print(f'{dta.strftime("%a")},{dta.strftime("%p")},{dta},'
              f'{dtz.strftime("%a")},{dtz.strftime("%p")},{dtz},'
              f'{delta},',
              f'{fmgr.get_message()},'
              f'{fmgr.get_activity()},'
              f'{fmgr.str_tags()}',
              file=ostrm)
        print(f'Elapsed H:M:S={delta} appended to {fcsv}')
    if not fmgr.get_keepstart():
        fmgr.rm_starttime()
    else:
        print('NOT restarting the timer because `--keepstart` invoked')


def _wr_csvhdrs(fcsv):
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
            'message,',
            'activity,',
            'tags',
            file=prt,
        )


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
