"""Print a time report"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"


FMT_STDOUT = '{Day:3}  {Date:10}  {Span:5}  {Total:>7}  {Description}'

def prt_basic(timefmtd):
    """Prints a basic time report to stdout"""
    assert timefmtd
    nt0 = timefmtd[0]
    flds = nt0._fields
    fmt = FMT_STDOUT
    print(fmt.format(**{f:f for f in flds}))
    for ntd in timefmtd:
        print(fmt.format(**ntd._asdict()))


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
