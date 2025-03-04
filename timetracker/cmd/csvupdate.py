"""Stop the timer and record this time unit"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
from os.path import relpath
from logging import debug
from datetime import datetime
from csv import reader
from timetracker.utils import yellow
from timetracker.consts import FMTDT
from timetracker.msgs import str_init
from timetracker.cfg.cfg_local  import CfgProj

def cli_run_csvupdate(cfglocal, args):
    """Stop the timer and record this time unit"""
    if args.input is not None and exists(args.input):
        update_csv(args.input, args.output)
        return
    run_csvupdate(
        cfglocal,
        args.name,
        args.output)

def run_csvupdate(fnamecfg, name, fout):
    """Stop the timer and record this time unit"""
    # Get the starting time, if the timer is running
    debug(yellow('RUNNING COMMAND CSVUPDATE'))
    if not exists(fnamecfg):
        print(str_init(fnamecfg))
        sys_exit(0)
    cfgproj = CfgProj(fnamecfg)


    fcsv = cfgproj.get_filename_csv(name)
    if fcsv is not None and exists(fcsv):
        debug(f'CSVUPDATE: CSVFILE   exists({int(exists(fcsv))}) {relpath(fcsv)}')
        update_csv(fcsv, fout)
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
    dta = datetime.strptime(row[2], FMTDT)
    dtz = datetime.strptime(row[5], FMTDT)
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
