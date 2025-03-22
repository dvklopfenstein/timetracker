"""CLI for examining how strings are converted to a datetime object using python-dateutil"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from dateutil.parser import parse as dateutil_parserdt
from dateutil.parser import ParserError
from dateutil.parser import UnknownTimezoneWarning
from timetracker.utils import white
from timetracker.utils import yellow

from timetracker.epoch.cli import run
from timetracker.epoch.epoch import get_dt_from_td


def main(arglist=None):
    """CLI for examining how strings are converted to a datetime object"""
    if run(arglist, get_dateutils_answer) is not None:
        sys_exit(0)
    sys_exit(1)  # Exited with error

def get_dateutils_answer(elapsed_or_dt, dta, defaultdt=None):
    """Get stop datetime, given a start time and a specific or elapsed time"""
    dto = get_dt_from_td(elapsed_or_dt, dta)
    if dto is not None:
        return dto
    try:
        #print(cyan(f'CCCCCCCCCCCCCC Using dateutil.parser({elapsed_or_dt}, default={defaultdt})'))
        return dateutil_parserdt(elapsed_or_dt, default=defaultdt)
    except (ParserError, UnknownTimezoneWarning) as err:
        print('ERROR FROM', white('python-dateutil: '), yellow(f'{err}'))
    print(f'"{elapsed_or_dt}" COULD NOT BE CONVERTED TO A DATETIME BY dateutils')
    return None



# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
