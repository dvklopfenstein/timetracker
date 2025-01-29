"""Stop the timer and record this time unit"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
from os.path import relpath
from logging import debug
from logging import error
from datetime import datetime
from csv import reader
from csv import DictReader
from csv import writer
##from timeit import default_timer
from timetracker.hms import read_startfile
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
        print(f'No project config file or csv file specified')
    elif not exists(fcsv):
        print(f'File, {fcsv}, does not exist')


def update_csv(fin_csv, fout_csv):
    """Update weekday, AM/PM, & duration using start_datetime and stop_datetime"""
    debug(f'update_csv(fin={fin_csv}, fout={fout_csv})')
    #with open(fout_csv, 'w', newline='', encoding='utf8') as ofstrm:
    with open(fin_csv, newline='', encoding='utf8') as ifstrm:
        csvreader = DictReader(ifstrm)
        #hdr = next(iter(csvreader))
        #                       0     1                 2           3     4                5           6          7           8         9
        #assert hdr == ['start_day', 'xm', 'start_datetime', 'stop_day', 'zm', 'stop_datetime', 'duration', 'message', ' activity', ' tags']
        #print(f'HEADER: {hdr}')
        for row in csvreader:
            start_datetime = datetime.strptime(row['start_datetime'], FMT)
            stop_datetime = datetime.strptime(row['stop_datetime'], FMT)
            print(start_datetime)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
