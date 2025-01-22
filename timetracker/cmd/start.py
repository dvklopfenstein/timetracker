"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
##from os.path import abspath
##from os.path import relpath
##from os.path import join
from logging import info

##from timeit import default_timer
##$from datetime import timedelta
from datetime import datetime


def run_start(fmgr):
    """Initialize timetracking on a project"""
    now = datetime.now()
    fin_start = fmgr.get_filename_start()
    # Print elapsed time, if timer was started
    fmgr.prt_elapsed()
    # Set/reset starting time, if applicable
    if not exists(fin_start) or fmgr.forced():
        fmgr.ini_workdir()
        with open(fin_start, 'w', encoding='utf8') as prt:
            prt.write(f'{now}')
            print(f'Timetracker started {now.strftime("%a %I:%M %p")}: {now}')
            info(f'  WROTE: {fin_start}')
    # Informational message
    elif not fmgr.forced():
        print('DO `trkr stop -m "task description"` to stop tracking this time unit')
        print('Do `trkr start --force`              to reset start time to now')
    else:
        print(f'Reseting start time to now({now})')


    #dirtrk = kws['directory']
    #if not exists(dirtrk):
    #    makedirs(dirtrk, exist_ok=True)
    #    absdir = abspath(dirtrk)
    #    print(f'Initialized empty timetracker directory: {absdir}')
    #    fout_cfg = join(absdir, 'config')
    #    with open(fout_cfg, 'w', encoding='utf8') as ostrm:
    #        print('', file=ostrm)
    #        print(f'  WROTE: {relpath(fout_cfg)}')


class CmdStart:
    """Initialize a timetracker project"""
    # pylint: disable=too-few-public-methods

    def __init__(self, cfgfile):
        self.cfgfile = cfgfile


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
