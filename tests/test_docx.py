#!/usr/bin/env python3
"""Test Timetracker use cases"""

#from os import environ
#from datetime import timedelta
#from timeit import default_timer
#from timetracker.consts import DIRTRK
#from timetracker.cli import Cli
from datetime import datetime
from datetime import timedelta
from timetracker.docx import WordDoc
from timetracker.csvfile import CsvFile
from timetracker.epoch.text import get_data_formatted
from tests.pkgtttest.cmpstr import get_filename

# pylint: disable=fixme


def test_docx():
    """Test Timetracker use cases"""
    filename = get_filename('docxtest.docx')
    doc = WordDoc(get_data_formatted(_get_datadt()))
    doc.write_doc(filename)
    # pylint: disable=line-too-long
    # make clobber

    # trk
    # Run `trk init` to initialize time-tracking for the project in

    # trk
    # Run `trk init` to initialize time-tracking for the project in

    # trk init
    # Initialized timetracker directory:

    # trk init
    # Trk repository already initialized:

    # trk start
    # Timetracker started Wed 03:21 PM: 2025-02-05 15:21:36.452917 for project 'timetracker' ID=username

    # trk start
    # Do `trk stop -m "task description"` to stop tracking this time unit

    # trk stop
    # usage: timetracker stop [-h] -m MESSAGE [--activity ACTIVITY] [-t [TAGS ...]]
    # timetracker stop: error: the following arguments are required: -m/--message

    # trk stop -m 'test stopped'
    # Timer stopped; Elapsed H:M:S=0:00:19.531226 appended to timetracker_timetracker_username.csv

def _get_datadt():
    # pylint: disable=line-too-long
    nto = CsvFile.nto
    return [
        nto(start_datetime=datetime(2025, 2, 14, 3, 53, 50, 828199), duration=timedelta(seconds=5724, microseconds=805698), message='Continue working on test; colorize, etc', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 14, 6, 20, 25, 667644), duration=timedelta(seconds=3123, microseconds=601581), message='csv test infrastructure', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 14, 11, 0, 35, 225588), duration=timedelta(seconds=35364, microseconds=127263), message='Working on csv tests', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 15, 5, 55, 33, 252411), duration=timedelta(seconds=1938, microseconds=606934), message='csv filename work; exp abs v rel', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 15, 6, 47, 46, 456123), duration=timedelta(seconds=1579, microseconds=989509), message='working on home ~ in csv', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 15, 11, 29, 15, 912609), duration=timedelta(seconds=16279, microseconds=165912), message='Worked on csv filename', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 18, 5, 48, 38, 71079), duration=timedelta(seconds=2500, microseconds=593462), message='Begin add time reporting command', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 18, 9, 24, 23, 81955), duration=timedelta(seconds=19202, microseconds=280988), message='wording in timer start message to be more clear', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 20, 13, 27, 0, 263091), duration=timedelta(seconds=5518, microseconds=877951), message='outerspace', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 21, 3, 53, 1, 398281), duration=timedelta(seconds=7162, microseconds=562427), message='Creating Epoch functionality for enhanced user experience', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 21, 10, 42, 10, 304621), duration=timedelta(days=1, seconds=672, microseconds=922163), message='Researchers will be able to enter tdeltas or dtimes in a human way', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 22, 10, 54, 15, 648891), duration=timedelta(seconds=5280, microseconds=639449), message='Created time-rounding class', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 22, 14, 28, 14, 597505), duration=timedelta(seconds=9371, microseconds=706075), message='Added ability to round dates to nearest specified minute', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 23, 2, 2, 44, 229235), duration=timedelta(seconds=14519, microseconds=679437), message='user-friendly time interval', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 23, 21, 5, 31, 975384), duration=timedelta(seconds=4564, microseconds=621763), message='M=README & setup', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 24, 0, 22, 1, 426463), duration=timedelta(seconds=6525, microseconds=100032), message='implemented getting epoch from researcher --epoch for the stop command', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 25, 10, 30), duration=timedelta(seconds=16200), message='`start --at is now fully tested`', activity='', tags=''),
        nto(start_datetime=datetime(2025, 2, 26, 1, 41, 53, 663646), duration=timedelta(seconds=10890, microseconds=395577), message='starting to generate a report', activity='', tags=''),
    ]


if __name__ == '__main__':
    test_docx()
