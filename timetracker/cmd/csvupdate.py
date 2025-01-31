"""Stop the timer and record this time unit"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
from os.path import relpath
from logging import debug
##from logging import error
from datetime import datetime
from csv import reader
##from csv import DictReader
##from csv import writer
##from timeit import default_timer
##from timetracker.hms import read_startfile
from timetracker.hms import FMT


def run_csvupdate(fmgr):
    """Stop the timer and record this time unit"""
    # Get the starting time, if the timer is running
    debug('CSVUPDATE: RUNNING COMMAND CSVUPDATE')
    cfgproj = fmgr.cfg
    args = fmgr.kws

    if args['input'] is not None:
        update_csv(args['input'], args['output'])
        sys_exit()

    fcsv = cfgproj.get_filename_csv()
    if fcsv is not None and exists(fcsv):
        debug(f'CSVUPDATE: CSVFILE   exists({int(exists(fcsv))}) {relpath(fcsv)}')
        update_csv(fcsv, args['output'])
    elif fcsv is None:
        print('No project config file or csv file specified')
    elif not exists(fcsv):
        print(f'File, {fcsv}, does not exist')


def update_csv(fin_csv, fout_csv):
    """Update weekday, AM/PM, & duration using start_datetime and stop_datetime"""
    debug(f'update_csv(fin={fin_csv}, fout={fout_csv})')
    # pylint: disable=fixme
    # pylint: disable=unused-variable
    # TODO: Finish implementing
    with open(fout_csv, 'w', newline='', encoding='utf8') as ofstrm:
        with open(fin_csv, newline='', encoding='utf8') as ifstrm:
            ##csvreader = DictReader(ifstrm)
            csvreader = reader(ifstrm)
            hdr = next(iter(csvreader))
            debug(f'HEADERS: {hdr}')
            # assert hdr == [
            #      'start_day',      #  0
            #      'xm',             #  1
            #      'start_datetime', #  2
            #      'stop_day',       #  3
            #      'zm',             #  4
            #      'stop_datetime',  #  5
            #      'duration',       #  6
            #      'message',        #  7
            #      'activity',       #  8
            #      'tags',           #  9
            # ]
            #print(f'HEADER: {hdr}')
            for rowvals_orig in csvreader:
                debug(f'VVVVVVVVVVVVVVVVVVVVV: {rowvals_orig}')
                rowvals_new = _get_rowvals(rowvals_orig)
                txt = ','.join(rowvals_new)
                debug(f'WWWWWWWWWWWWWWWWWWWWW: {rowvals_new}')
            debug(f'READ:  {fin_csv}')
        debug(f'WROTE: {fout_csv}')

def _get_rowvals(row):
    dta = datetime.strptime(row[2], FMT)
    dtz = datetime.strptime(row[5], FMT)
    delta = dtz - dta
    return (
        dta.strftime("%a"), # 0 updated
        dta.strftime("%p"), # 1 updated
        row[2],             # 2
        dtz.strftime("%a"), # 3 updated
        dtz.strftime("%p"), # 4 updated
        row[5],             # 5
        str(delta),         # 6 updated
        row[7],             # 7
        row[8],             # 8
        row[9],             # 9
    )


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
