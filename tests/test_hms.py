#!/usr/bin/env python3
"""Test writing elapsed times into a timetracking file"""

##from os import system
from time import sleep
from timeit import default_timer
from timetracker.hms import str_hms_tic


def test_hms():
    """Test writing elapsed times into a timetracking file"""

    tic = default_timer()
    sleep(1)
    print(str_hms_tic(tic))


if __name__ == '__main__':
    test_hms()
