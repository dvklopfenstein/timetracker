#!/usr/bin/env python3
"""Test writing elapsed times into a timetracking file"""

from os import system
from time import sleep
from timetracker.recorder import Recorder


def test_timetracker():
    """Test writing elapsed times into a timetracking file"""
    csv = 'test_timetracker.csv'
    obj = Recorder(csv)
    obj.start()
    sleep(1)
    obj.stop("Stopped after 1 seconds")
    system(f'cat {csv}')


if __name__ == '__main__':
    test_timetracker()
