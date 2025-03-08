"""Epoch: an extent of time associated with a particular person or thing.

“Epoch.” Merriam-Webster's Collegiate Thesaurus, Merriam-Webster,
 https://unabridged.merriam-webster.com/thesaurus/epoch.
 Accessed 21 Feb. 2025.

https://github.com/onegreyonewhite/pytimeparse2/issues/11
https://github.com/dateutil/dateutil/
"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from datetime import datetime
from datetime import timedelta
from pytimeparse2 import parse as pyt2_parser_secs
from dateutil.parser import parse as dateutil_parserdt
from dateutil.parser import ParserError
from dateutil.parser import UnknownTimezoneWarning
from timetracker.timecalc import RoundTime
from timetracker.consts import FMTDT_H
#from timetracker.utils import cyan
from timetracker.utils import orange


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


####def get_dtz(epochstr, dta, defaultdt=None):
####    """Get stop datetime, given a start time and a specific or elapsed time"""
####    try:
####        return Epoch(epochstr, dta, defaultdt).get_dtz()
####    except TypeError as err:
####        raise RuntimeError('ERROR RUNNING get_dtz(...):\n  '
####            f'string        : {epochstr},\n  '
####            f'from datetime : {dta})') from err

def get_dtz(elapsed_or_dt, dta, defaultdt=None):
    """Get stop datetime, given a start time and a specific or elapsed time"""
    if elapsed_or_dt.count(':') != 2:
        #print(cyan(f'AAAAAAAAAAAAAA Using pytimeparse2({elapsed_or_dt}) + {dta}'))
        secs = _conv_timedelta(elapsed_or_dt)
        #print(cyan(f'BBBBBBBBBBBBBB secs = {secs}'))
        if secs is not None:
            return dta + timedelta(seconds=secs)
    try:
        #print(cyan(f'CCCCCCCCCCCCCC Using dateutil.parser({elapsed_or_dt}, default={defaultdt})'))
        return dateutil_parserdt(elapsed_or_dt, default=defaultdt)
    except (ParserError, UnknownTimezoneWarning) as err:
        print(orange(f'ERROR: {err}'))
    print(f'"{elapsed_or_dt}" COULD NOT BE CONVERTED TO A TIME')
    return None

def _conv_timedelta(elapsed_or_dt):
    try:
        return pyt2_parser_secs(elapsed_or_dt)
    except TypeError as err:
        raise RuntimeError(f'UNABLE TO CONVERT str({elapsed_or_dt}) '
                            'TO A timedelta object') from err

####def is_datetime(self):
####    """Check if epoch is a datetime, rather than an elapsed time"""
####    epoch = self.estr
####    if epoch[:1] in {'\\', '~'}:
####        return False
####    if '-' in epoch:
####        return True
####    epoch = epoch.lower()
####    if 'am' in epoch:
####        return True
####    if 'pm' in epoch:
####        return True
####    return False

####class Epoch:
####    """Epoch: an extent of time associated with a particular person or thing"""
####    # pyli
####
####    def __init__(self, elapsed_or_dt, dta, defaultdt):
####        self.estr = elapsed_or_dt
####        self.dta = dta
####        self.tdflt = defaultdt
####
####    ####def get_dtz(self):
####    ####    """Get the ending time, given an epoch string"""
####    ####    return self._conv_datetime2() #if self.is_datetime() else self.conv_tdelta()
####    ####    #return self._conv_datetime() if self.is_datetime() else self.conv_tdelta()
####
####    def _conv_tdelta(self):
####        """Get the ending time, given an estr timedelta and a start time"""
####        secs = self._conv_timedelta()
####        if secs is not None:
####            return self.dta + timedelta(seconds=secs)
####        raise RuntimeError(f'STRING "{self.estr}" COULD NOT BE CONVERTED TO A timedelta')
####
####    ####def _conv_datetime(self):
####    ####    try:
####    ####        return dateutil_parserdt(self.estr, default=self.tdflt)
####    ####    except TypeError as err:
####    ####        raise RuntimeError(f'UNABLE TO CONVERT str({self.estr}) '
####    ####                            'TO A datetime object') from err
####
####    def get_dtz(self):
####        """GET dtz"""
####        try:
####            return dateutil_parserdt(self.estr, default=self.tdflt)
####        except (ParserError, UnknownTimezoneWarning) as err:
####            return self._conv_tdelta()
####
####    def _conv_timedelta(self):
####        try:
####            estr = self.estr
####            estr1 = estr[:1]
####            if estr1 not in {'~', '\\'}:
####                return pyt2_parser_secs(estr)
####            if estr1 == '~':
####                return -pyt2_parser_secs(estr[1:])
####            return -pyt2_parser_secs(estr[2:])
####        except TypeError as err:
####            raise RuntimeError(f'UNABLE TO CONVERT str({self.estr}) '
####                                'TO A timedelta object') from err
####
####    ####def is_datetime(self):
####    ####    """Check if epoch is a datetime, rather than an elapsed time"""
####    ####    epoch = self.estr
####    ####    if epoch[:1] in {'\\', '~'}:
####    ####        return False
####    ####    if '-' in epoch:
####    ####        return True
####    ####    epoch = epoch.lower()
####    ####    if 'am' in epoch:
####    ####        return True
####    ####    if 'pm' in epoch:
####    ####        return True
####    ####    return False


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
