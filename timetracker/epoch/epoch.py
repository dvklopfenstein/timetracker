"""Epoch: an extent of time associated with a particular person or thing.

“Epoch.” Merriam-Webster's Collegiate Thesaurus, Merriam-Webster,
 https://unabridged.merriam-webster.com/thesaurus/epoch.
 Accessed 21 Feb. 2025.

https://github.com/onegreyonewhite/pytimeparse2/issues/11
https://github.com/scrapinghub/dateparser
"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from datetime import datetime
from datetime import date
from datetime import timedelta
#from timeit import default_timer  # PRT
from pytimeparse2 import parse as pyt2_parse_secs
import dateparser
from timetracker.epoch.calc import RoundTime
from timetracker.epoch.stmach import search_texttime
from timetracker.consts import FMTDT_H


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


def get_dt_at(time_at=None, now=None, defaultdt=None):
    """Get time as now or as time_at"""
    if now is None:
        now = get_now()
    return now if time_at is None else get_dtz(time_at, now, defaultdt)

def get_now():
    """Get the date and time as of right now"""
    return datetime.now()

def get_dtz(elapsed_or_dt, dta, defaultdt=None):
    """Get stop datetime, given a start time and a specific or elapsed time"""
#    _get_dt_ampm(elapsed_or_dt, defaultdt)  # PRT
    if (dto := _get_dt_ampm(elapsed_or_dt, defaultdt)) is not None:
        return dto
    if (dto := _get_dt_from_td(elapsed_or_dt, dta)) is not None:
        return dto
    return _conv_datetime(elapsed_or_dt, defaultdt)

def _conv_datetime(timestr, defaultdt):
    try:
        settings = None if defaultdt is None else {'RELATIVE_BASE': defaultdt}
#        tic = default_timer()  # PRT
        dto = dateparser.parse(timestr, settings=settings)
#        print(f'{timedelta(seconds=default_timer()-tic)} dateparser   parse({timestr})')  # PRT
#        if dto is None:  # PRT
#            print(f'ERROR: text({timestr}) could not be converted to a datetime object')  # PRT
        return dto
    except (ValueError, TypeError, dateparser.conf.SettingValidationError) as err:
        print(f'ERROR FROM python-dateparser: {err}')
    print(f'"{timestr}" COULD NOT BE CONVERTED TO A DATETIME BY dateparsers')
    return None

def _get_dt_ampm(elapsed_or_dt, defaultdt):
    """Get a datetime object from free text that contains AM/PM"""
#    tic = default_timer()  # PRT
#    print(f'TEXT({elapsed_or_dt})')  # PRT
    ret = None
    if (mtch := search_texttime(elapsed_or_dt)) is not None and 'hour' in mtch:
#        print(f'{timedelta(seconds=default_timer()-tic)} parse({elapsed_or_dt}) SM')  # PRT
        _get_ymd(mtch, defaultdt)
#        print(f'{timedelta(seconds=default_timer()-tic)} parse({elapsed_or_dt}) today()')  # PRT
        ret = datetime(year=mtch['year'], month=mtch['month'], day=mtch['day'],
                       hour=mtch['hour'],
                       minute=mtch.get('minute', 0),
                       second=mtch.get('second', 0))
#    print(f'{timedelta(seconds=default_timer()-tic)} parse({elapsed_or_dt}) new datetime')  # PRT
    return ret

def _get_ymd(mtch, defaultdt):
    if {'year', 'month', 'day'}.issubset(set(mtch.keys())):
        return
    today = date.today() if defaultdt is None else defaultdt
#    print(f'DEFAULTDT: {today}')  # PRT
    if 'year' not in mtch:
        mtch['year']  = today.year
    if 'month' not in mtch:
        mtch['month'] = today.month
    if 'day' not in mtch:
        mtch['day']   = today.day

def _get_dt_from_td(elapsed_or_dt, dta):
    """Get a datetime object from a timedelta time string"""
    if elapsed_or_dt.count(':') != 2 and (secs := _conv_timedelta(elapsed_or_dt)):
        return dta + timedelta(seconds=secs)
    return None

def _conv_timedelta(timestr):
    try:
#        tic = default_timer()  # PRT
        ret = pyt2_parse_secs(timestr)
#        print(f'{timedelta(seconds=default_timer()-tic)} pytimeparse2 parse({timestr})')  # PRT
        return ret
    except TypeError as err:
        raise RuntimeError(f'UNABLE TO CONVERT str({timestr}) '
                            'TO A timedelta object') from err

# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
