"""CLI for examining how strings are converted to a datetime object"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from datetime import datetime
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from timetracker.epoch.epoch import get_dtz


def main(arglist=None):
    """CLI for examining how strings are converted to a datetime object"""
    if run(arglist) is not None:
        sys_exit(0)
    sys_exit(1)  # Exited with error

def run(arglist=None):
    """CLI for examining how strings are converted to a datetime object"""
    args = _get_args(arglist)
    #print(f'ARGS: {args}')
    dto = get_dtz(args.timetext, args.now, args.defaultdt)
    if dto is not None:
        ret = _prt(dto, f'<- "{args.timetext}"', args.formatcode)
        if args.now:
            _prt(datetime.now(), '<- now', args.formatcode)
        return ret
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
    parser.add_argument('-n', '--now', action='store_true',
        help="Print the current datetime as well as the converted `timetext`")
    parser.add_argument('--setnow',
        help="datetime representing `now`")
    parser.add_argument('-d', '--defaultdt',
        help="datetime representing a default to pass to dateutil")
    return parser.parse_args(arglist)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
