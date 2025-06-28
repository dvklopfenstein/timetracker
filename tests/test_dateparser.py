#!/usr/bin/env python
"""Code for dateparser issue: https://github.com/scrapinghub/dateparser/issues/1266"""
# https://github.com/scrapinghub/dateparser/pull/1274

from datetime import datetime
from dateparser import parse


CALSTR = """
December 2024
 Su  Mo  Tu  We  Th  Fr  Sa
(29) 30  31  [1]  2   3   4
 Su  Mo  Tu  We  Th  Fr  Sa
         January 2025
"""


def test_dateparser():
    """#1266: parse returns wrong month when using RELATIVE_BASE"""
    base = datetime(2025, 1, 1)
    timestr = 'Sun 9am'
    date = parse(timestr, settings={'RELATIVE_BASE': base})
    print(f'{base}: RELATIVE_BASE Wed Jan 1, 2025')
    print(f'{date}: "{timestr}"')

    # UNCOMMENT WHEN dateparser FIX IS RELEASED:
    #   https://github.com/scrapinghub/dateparser/pull/1274
    assert date == datetime(2024, 12, 29, 9), (
        f'GitHub issue https://github.com/scrapinghub/dateparser/issues/1266\n'
        f'{CALSTR}\n'
        'If today  is Wed, Jan 1, 2025;\n'
        f'then "{timestr}" is Sun, Dec 29, 2024\n\n'
        f'EXP: "2024-12-29 09:00:00"\n'
        f'ACT: "{date}"'
        )

    # THIS IS INCORRECT, BUT THAT IS WHAT COMES OUT WITH OLD dateparser
    #assert date == datetime(2024, 1, 29, 9)


if __name__ == '__main__':
    test_dateparser()
