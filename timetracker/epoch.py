"""Epoch: an extent of time associated with a particular person or thing.

“Epoch.” Merriam-Webster's Collegiate Thesaurus, Merriam-Webster, 
 https://unabridged.merriam-webster.com/thesaurus/epoch.
 Accessed 21 Feb. 2025.
"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from datetime import datetime
from datetime import timedelta
from timetracker.timecalc import RoundTime
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
    'Use `--epoch` or `-e` to specify an elapsed time (since '
    f'{dtval.strftime(dtfmt) if dtval is not None else "the start time"}):\n'
    f'    --epoch "30 minutes" # 30 minutes{desc}; Human-readable format\n'
    f'    --epoch "30 min"     # 30 minutes{desc}; Human-readable format\n'
    f'    --epoch "00:30:00"   # 30 minutes{desc}; Hour:minute:second format\n'
    f'    --epoch "30:00"      # 30 minutes{desc}; Hour:minute:second format, shortened\n'
    '\n'
    f'    --epoch "4 hours"    # 4 hours{desc}; Human-readable format\n'
    f'    --epoch "04:00:00"   # 4 hours{desc}; Hour:minute:second format\n'
    f'    --epoch "4:00:00"    # 4 hours{desc}; Hour:minute:second format, shortened\n'
    '\n'
    'Or use `--epoch` or `-e` to specify a start or stop datetime:\n'
    f'''    --epoch "{dtp.strftime('%Y-%m-%d %H:%M:%S')}"    '''
    '# datetime format, 24 hour clock shortened\n'
    f'''    --epoch "{dtp.strftime('%Y-%m-%d %I:%M:%S %p').lower()}" '''
    '# datetime format, 12 hour clock\n'
    f'''    --epoch "{dtp.strftime('%m-%d %H:%M:%S')}"         '''
    '# this year, datetime format, 24 hour clock shortened\n'
    f'''    --epoch "{dtp.strftime('%m-%d %I:%M:%S %p').lower()}"      '''
    '# this year, datetime format, 12 hour clock\n'

    f'''    --epoch "{dtp2.strftime('%m-%d %I%p').lower().replace(' 0', ' ')}"\n'''
    f'''    --epoch "{dtp.strftime('%m-%d %I:%M %p').lower().replace(' 0', ' ')}"\n'''
    f'''    --epoch "{dtp2.strftime('%m-%d %I:%M %p').lstrip("0").lower().replace(' 0', ' ')}""\n'''
    f'''    --epoch "{dtp.strftime('%I:%M %p').lstrip("0").lower().replace(' 0', ' ')}"       '''
    '# Today\n'
    f'''    --epoch "{dtp2.strftime('%I:%M %p').lstrip("0").lower().replace(' 0', ' ')}"       '''
    '# Today\n'
    )


class Epoch:
    """Epoch: an extent of time associated with a particular person or thing"""

    def __init__(self, elapsed_or_dt):
        self.epoch = elapsed_or_dt

    def is_datetime(self):
        """Check if epoch is a datetime, rather than an elapsed time"""
        epoch = self.epoch.lower()
        if '-' in epoch:
            return True
        if 'am' in epoch:
            return True
        if 'pm' in epoch:
            return True
        return False

    @staticmethod
    def get_today():
        """Get today's date without the time"""
        # pylint: disable=line-too-long
        # https://stackoverflow.com/questions/6545254/difference-between-system-datetime-now-and-system-datetime-today
        # https://codeofmatt.com/the-case-against-datetime-now/
        #return DateTimeOffset.Now
        return datetime.today()


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
