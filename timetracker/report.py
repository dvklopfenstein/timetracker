"""Print a time report"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

#from os import remove
#from os.path import exists
#from os.path import basename
#from os.path import join
#from os.path import abspath
#from os.path import dirname
#from os.path import normpath
#from datetime import timedelta
#from datetime import datetime
#from logging import debug
#from csv import reader

#from timetracker.utils import orange
#from timetracker.consts import DIRTRK
#from timetracker.consts import FMTDT
#from timetracker.cfg.utils import get_username


class Report:
    """Print a time report"""
    # pylint: disable=too-few-public-methods

    FMT_STDOUT = '{Day:3}  {Date:10}  {Span:5}  {Total:>7}  {Description}'

    def __init__(self, timefmtd):
        self.timefmtd = timefmtd
        assert timefmtd, 'No formatted time records'

    def prt_basic(self):
        """Prints a basic time report to stdout"""
        nt0 = self.timefmtd[0]
        flds = nt0._fields
        fmt = self.FMT_STDOUT
        print(fmt.format(**{f:f for f in flds}))
        for ntd in self.timefmtd:
            print(fmt.format(**ntd._asdict()))


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
