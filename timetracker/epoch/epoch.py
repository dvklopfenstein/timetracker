"""Epoch: an extent of time associated with a particular person or thing.

“Epoch.” Merriam-Webster's Collegiate Thesaurus, Merriam-Webster,
 https://unabridged.merriam-webster.com/thesaurus/epoch.
 Accessed 21 Feb. 2025.

https://github.com/onegreyonewhite/pytimeparse2/issues/11
https://github.com/scrapinghub/dateparser
"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from logging import debug
from datetime import datetime
from datetime import timedelta
from pytimeparse2 import parse as pyt2_parse_secs
from dateparser import parse as dateparser_parserdt
from dateparser.conf import SettingValidationError
from timetracker.epoch.calc import RoundTime
from timetracker.consts import FMTDT_H
from timetracker.utils import white
from timetracker.utils import yellow
from timetracker.utils import cyan


def str_arg_epoch(dtval=None, dtfmt=None, desc=''):
    """Get instructions on how to specify an epoch"""
    if dtfmt is None:
        dtfmt = FMTDT_H
    if dtval is None:
        dtval = datetime.now()
    round30min = RoundTime(30)
    dtp = round30min.time_ceil(dtval + timedelta(minutes=90))
    dtp2 = round30min.time_ceil(dtval + timedelta(minutes=120))
    return (
    '\n'
    'Use `--at` or `-@` to specify an elapsed time (since '
    f'{dtval.strftime(dtfmt) if dtval is not None else "the start time"}):\n'
    f'    --at "30 minutes" # 30 minutes{desc}; Human-readable format\n'
    f'    --at "30 min"     # 30 minutes{desc}; Human-readable format\n'
    f'    --at "00:30:00"   # 30 minutes{desc}; Hour:minute:second format\n'
    f'    --at "30:00"      # 30 minutes{desc}; Hour:minute:second format, shortened\n'
    '\n'
    f'    --at "4 hours"    # 4 hours{desc}; Human-readable format\n'
    f'    --at "04:00:00"   # 4 hours{desc}; Hour:minute:second format\n'
    f'    --at "4:00:00"    # 4 hours{desc}; Hour:minute:second format, shortened\n'
    '\n'
    'Or use `--at` or `-@` to specify a start or stop datetime:\n'
    f'''    --at "{dtp.strftime('%Y-%m-%d %H:%M:%S')}"    '''
    '# datetime format, 24 hour clock shortened\n'
    f'''    --at "{dtp.strftime('%Y-%m-%d %I:%M:%S %p').lower()}" '''
    '# datetime format, 12 hour clock\n'
    f'''    --at "{dtp.strftime('%m-%d %H:%M:%S')}"         '''
    '# this year, datetime format, 24 hour clock shortened\n'
    f'''    --at "{dtp.strftime('%m-%d %I:%M:%S %p').lower()}"      '''
    '# this year, datetime format, 12 hour clock\n'

    f'''    --at "{dtp2.strftime('%m-%d %I%p').lower().replace(' 0', ' ')}"\n'''
    f'''    --at "{dtp.strftime('%m-%d %I:%M %p').lower().replace(' 0', ' ')}"\n'''
    f'''    --at "{dtp2.strftime('%m-%d %I:%M %p').lstrip("0").lower().replace(' 0', ' ')}""\n'''
    f'''    --at "{dtp.strftime('%I:%M %p').lstrip("0").lower().replace(' 0', ' ')}"       '''
    '# Today\n'
    f'''    --at "{dtp2.strftime('%I:%M %p').lstrip("0").lower().replace(' 0', ' ')}"       '''
    '# Today\n'
    )


def get_dtz(elapsed_or_dt, dta, defaultdt=None):
    """Get stop datetime, given a start time and a specific or elapsed time"""
    dto = get_dt_from_td(elapsed_or_dt, dta)
    if dto is not None:
        return dto
    try:
        debug(cyan(f'CCCCCCCCCCCCCC Using dateparser.parser({elapsed_or_dt}, default={defaultdt})'))
        settings = None if defaultdt is None else {'RELATIVE_BASE': defaultdt}
        dto = dateparser_parserdt(elapsed_or_dt, settings=settings)
        if dto is None:
            print(f'warning: text({elapsed_or_dt}) could not be converted to a datetime object')
        debug(f'dto({dto})')
        return dto
    except (ValueError, TypeError, SettingValidationError) as err:
        print('ERROR FROM', white('python-dateparser: '), yellow(f'{err}'))
    print(f'"{elapsed_or_dt}" COULD NOT BE CONVERTED TO A DATETIME BY dateparsers')
    return None

def get_dt_from_td(elapsed_or_dt, dta):
    """Get a datetime object from a timedelta time string"""
    if elapsed_or_dt.count(':') != 2:
        debug(cyan(f'AAAAAAAAAAAAAA Using pytimeparse2({elapsed_or_dt}) + {dta}'))
        secs = _conv_timedelta(elapsed_or_dt)
        debug(cyan(f'BBBBBBBBBBBBBB secs = {secs}'))
        if secs is not None:
            return dta + timedelta(seconds=secs)
    return None

def _conv_timedelta(elapsed_or_dt):
    try:
        return pyt2_parse_secs(elapsed_or_dt)
    except TypeError as err:
        raise RuntimeError(f'UNABLE TO CONVERT str({elapsed_or_dt}) '
                            'TO A timedelta object') from err


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
