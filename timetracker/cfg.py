"""Configuration parser for timetracking.

Uses https://github.com/python-poetry/tomlkit,
but will switch to tomllib in builtin to standard Python (starting 3.11)
in a version supported by cygwin, conda, and venv.

"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import environ
from os.path import expanduser
from os.path import exists
from os.path import join
from tomlkit import comment
from tomlkit import document
from tomlkit import nl
from tomlkit import table
from tomlkit import dumps


class Cfg:
    """Configuration parser for timetracking"""
    # pylint: disable=too-few-public-methods

    DIR = './.timetracker'
    CSVPAT = 'timetracker_PROJECT_USER.csv'

    def __init__(self, name=None):
        self.cfg_global = self._init_cfgglobal()
        self.cfg_local = self._init_cfglocal()
        self.name = environ.get('USER') if name is not None else name
        self.doc = self._init_localdoc()

    def str_cfg(self):
        """Return string containing configuration file contents"""
        return dumps(self.doc)

    def wr_cfg(self, fname):
        """Write config file"""
        with open(fname, 'w', encoding='utf8') as ostrm:
            print(dumps(self.doc), file=ostrm)

    def _init_localdoc(self):
        doc = document()
        doc.add(comment("TimeTracker config file"))
        doc.add(nl())
        doc["title"] = "TimeTracker"

        # [csv]
        # directory = "./.timetracker"
        # format = "timetracker_dvklo.csv"
        csv_section = table()
        csv_format = self.CSVPAT
        if self.name:
            csv_format = csv_format.replace('USER', self.name)
        #csvdir.comment("Directory where the csv file is stored")
        csv_section.add("filename", join(self.DIR, csv_format))
        ##csv_section["csv_dir"].comment('Directory for the local config file')
        ##
        ### Adding the table to the document
        doc.add("csv", csv_section)

        return doc

    def _init_cfgglobal(self):
        fname = expanduser('~/.timetrackerconfig')
        print(f'GLOBAL CONFIG({fname})')
        return fname if exists(fname) else None

    def _init_cfglocal(self):
        fname = expanduser(join(self.DIR, 'config'))
        print(f'LOCAL  CONFIG({fname})')
        return fname if exists(fname) else None


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
