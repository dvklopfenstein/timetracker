"""Local project configuration parser for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import remove
from os.path import exists
from os.path import basename
from os.path import join
from os.path import abspath
from os.path import dirname
from os.path import normpath
from datetime import datetime
from logging import debug

from timetracker.utils import orange
from timetracker.consts import DIRTRK
from timetracker.cfg.utils import get_username


class CsvFile:
    """Manage CSV file"""

    def __init__(self, csvfilename):
        self.fcsv = csvfilename
        debug(orange(f'Starttime args {int(exists(self.fcsv))} self.fcsv {self.fcsv}'))

    #def get_desc(self, note=' set'):
    #    """Get a string describing the state of an instance of the CfgProj"""
    #    return (
    #        f'CfgProj {note} {int(exists(self.filename))} '
    #        f'fname start {self.filename}')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
