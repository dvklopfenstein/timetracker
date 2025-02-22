"""Epoch: an extent of time associated with a particular person or thing.

“Epoch.” Merriam-Webster's Collegiate Thesaurus, Merriam-Webster, 
 https://unabridged.merriam-webster.com/thesaurus/epoch.
 Accessed 21 Feb. 2025.
"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from datetime import datetime
from timetracker.consts import FMTDT_H


def str_arg_epoch(dtval=None, dtfmt=None):
    """Get instructions on how to specify an epoch"""
    if dtfmt is None:
        dtfmt = FMTDT_H
    # pylint: disable=fixme
    # TODO: Base epoch dt example on dtval
    return (
    '\n'
    'Use `--epoch` or `-e` to specify an elapsed time (since '
    f'{dtval.strftime(dtfmt) if dtval is not None else "the start time"}):\n'
    '    --epoch "30 minutes" # Human-readable format\n'
    '    --epoch "30 min"     # Human-readable format\n'
    '    --epoch "00:30:00"   # Hour:minute:second format\n'
    '    --epoch "30:00"      # Hour:minute:second format, shortened\n'
    '\n'
    '    --epoch "4 hours"    # Human-readable format\n'
    '    --epoch "04:00:00"   # Hour:minute:second format\n'
    '    --epoch "4:00:00"    # Hour:minute:second format, shortened\n'
    '\n'
    'Or use `--epoch` or `-e` to specify a start or stop datetime:\n'
    '    --epoch "2025-02-19 15:30:00.243778" # datetime format, 24 hour clock (default)\n'
    '    --epoch "2025-02-19 15:30:00"        # datetime format, 24 hour clock shortened\n'
    '    --epoch "2025-02-19 03:30:00 pm"     # datetime format, 12 hour clock\n'
    '    --epoch "02-19 15:30:00"     # this year, datetime format, 24 hour clock shortened\n'
    '    --epoch "02-19 03:30:00 pm"  # this year, datetime format, 12 hour clock\n'
    '    --epoch "02-19 3pm"          # this year, 12 hour clock\n'
    '    --epoch "02-19 3:30pm"       # this year, 12 hour clock\n'
    '    --epoch "2-19 3:30pm"        # this year, 12 hour clock\n'
    '    --epoch "3pm"                # today, 12 hour clock\n'
    '    --epoch "3:30pm"             # today, 12 hour clock\n'
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
