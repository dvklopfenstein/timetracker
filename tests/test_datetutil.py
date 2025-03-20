#!/usr/bin/env python3
"""Test dateutil interpreting 5pm.
https://github.com/dateutil/dateutil/issues/1421

Other issues that make python-dateutil not good for this project:
    * Interprets "Tue" as "next Tuesday"
    * Does not recognize "last Tuesday"
    * Does not recognize "next Tuesday"
"""

from datetime import datetime
from dateutil.parser import parse


def test_dateutil():
    """Test dateutil interpreting 5pm"""
    defaultdt = datetime(2025, month=1, day=1, hour=8, minute=15)

    dt5  = parse("01-1 5pm")
    dt5a = parse("01-1 5pm", default=defaultdt)

    print(dt5)
    print(dt5a)
    # pylint: disable=fixme
    # TODO: If dateutil issue 1421 is fixed, uncomment
    #assert dt5 == dt5a


if __name__ == '__main__':
    test_dateutil()
