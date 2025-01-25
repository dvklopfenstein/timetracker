"""Stop the timer and record this time unit"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from os.path import relpath
from logging import error
from datetime import datetime
##from timeit import default_timer
from timetracker.hms import read_startfile


def run_stop(fmgr):
    """Stop the timer and record this time unit"""
    # Get the starting time, if the timer is running
    dta = read_startfile(fmgr.get_filename_start())
    if dta is None:
        error('NOT WRITING ELAPSED TIME; Do `trkr start` to begin tracking time')
        return

    # Append the timetracker file with this time unit
    fcsv = fmgr.get_filename_csv()
    if not exists(fcsv):
        _wr_csvlong_hdrs(fcsv)
    _wr_csvlong_data(fcsv, fmgr, dta)
    if not fmgr.get("keepstart"):
        fmgr.rm_starttime()
    else:
        print('NOT restarting the timer because `--keepstart` invoked')

def _wr_csv_data(fcsv, fmgr, dta):
    with open(fcsv, 'a', encoding='utf8') as ostrm:
        ##toc = default_timer()
        dtz = datetime.now()
        delta = dtz - dta
        print(f'{dta.strftime("%a")},{dta.strftime("%p")},{dta},'
              f'{dtz.strftime("%a")},{dtz.strftime("%p")},{dtz},'
              f'{delta},'
              f'{fmgr.get("message")},'
              f'{fmgr.get("activity")},'
              f'{fmgr.str_tags()}',
              file=ostrm)
        if not fmgr.get('quiet'):
            print(f'Timer stopped; Elapsed H:M:S={delta} appended to {fcsv}')

def _wr_csvlong_data(fcsv, fmgr, dta):
    with open(fcsv, 'a', encoding='utf8') as ostrm:
        dtz = datetime.now()
        delta = dtz - dta
        print(f'{dta.strftime("%a")},{dta.strftime("%p")},{dta},'
              f'{dtz.strftime("%a")},{dtz.strftime("%p")},{dtz},'
              f'{delta},'
              f'{fmgr.get("message")},'
              f'{fmgr.get("activity")},'
              f'{fmgr.str_tags()}',
              file=ostrm)
        if not fmgr.get('quiet'):
            print(f'Timer stopped; Elapsed H:M:S={delta} appended to {relpath(fcsv)}')

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
            'message,',
            'activity,',
            'tags',
            file=prt,
        )


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
