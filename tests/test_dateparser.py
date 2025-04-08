#!/usr/bin/env python
"""Code for dateparser issue: https://github.com/scrapinghub/dateparser/issues/1266"""

from datetime import datetime
from dateparser import parse


def test_dateparser():
    """#1266: parse returns wrong month when using RELATIVE_BASE"""
    base = datetime(2025, 1, 1)
    timestr = 'Sun 9am'
    date = parse(timestr, settings={'RELATIVE_BASE': base})
    print(f'{base}: BASE DATE')
    print(f'{date}: {timestr}')


if __name__ == '__main__':
    test_dateparser()
