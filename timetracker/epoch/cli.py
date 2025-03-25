"""CLI for examining how strings are converted to a datetime object"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from logging import debug
from datetime import datetime
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from timetracker.epoch.epoch import get_dtz
from timetracker.epoch.calc import dt_from_str


def main(arglist=None):
    """CLI for examining how strings are converted to a datetime object"""
    if run(arglist, get_dtz) is not None:
        sys_exit(0)
    sys_exit(1)  # Exited with error


def run(arglist=None, fnc=None):
    """CLI for examining how strings are converted to a datetime object"""
    args = _get_args(arglist)
    debug(f'ARGS: {args}')
    now = datetime.now()
    if args.now is not None:
        now = fnc(args.now, now)
    defaultdt = None if args.defaultdt is None else dt_from_str(args.defaultdt)
    debug(f'DEFAULTDT: {type(defaultdt)}')
    dto = fnc(args.timetext, now, defaultdt)
    if dto is not None:
        ret = _prt(dto, f'<- "{args.timetext}"', args.formatcode)
        _prt(now, '<- now', args.formatcode)
        return ret
    print(f'**FATAL: UNABLE TO CONVERT TEXT({args.timetext})')
    return None

def _prt(dto, desc, formatcode):
    dtprt = str(dto) if formatcode is None else dto.strptime(formatcode)
    print(f'{dtprt:26} {desc}')
    return dtprt

def _get_args(arglist=None):
    """Get arguments for examining how strings are converted to a datetime object"""
    parser = ArgumentParser(
        prog="parsedate",
        description="Print a datetime object, given free text",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('timetext',
        help='Text to convert to a datetime object')
    parser.add_argument('-f', '--formatcode',
        help=("Format the datetime object using "
              "https://docs.python.org/3/library/datetime.html#format-codes"))
    parser.add_argument('-n', '--now',
        help="Print the current datetime as well as the converted `timetext`")
    parser.add_argument('-d', '--defaultdt',
        help=('default to pass to datetime parser, '
              'eg "2025-03-20 09:00:00" or "2025-03-20 09:00:00.000001"'))
    return parser.parse_args(arglist)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
