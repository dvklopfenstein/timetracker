#!/usr/bin/env python
"""Code for dateparser issue: https://github.com/scrapinghub/dateparser/issues/1266"""

from datetime import datetime
from dateparser import parse


def test_dateparser():
    """#1266: parse returns wrong month when using RELATIVE_BASE"""
    base = datetime(2025, 1, 1)
    timestr = 'Sun 9am'
    date = parse(timestr, settings={'RELATIVE_BASE': base})
    print(f'{base}: RELATIVE_BASE')
    print(f'{date}: "{timestr}"')
    #assert date == datetime(2024, 12, 29, 9) #1266
    assert date == datetime(2024, 1, 29, 9)


if __name__ == '__main__':
    test_dateparser()
