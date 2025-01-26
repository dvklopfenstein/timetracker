"""Configuration parser for timetracking.

Uses https://github.com/python-poetry/tomlkit,
but will switch to tomllib in builtin to standard Python (starting 3.11)
in a version supported by cygwin, conda, and venv.

"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import environ
from os import getcwd
from os.path import basename
from os.path import expanduser
from os.path import join
from os.path import abspath
from os.path import relpath
from os.path import normpath
from logging import debug
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
        self.cfg_global = expanduser('~/.timetrackerconfig')
        self.cfg_local = expanduser(join(self.DIR, 'config'))
        self.project = basename(getcwd())
        self.name = environ.get('USER') if name is None else name
        self.csv_dir = self.DIR
        self.csv_name = self.CSVPAT.replace('PROJECT', self.project).replace('USER', self.name)
        self.docloc = self._init_localdoc()
        debug(f'CFG LOCAL  CONFIG({self.cfg_global})')
        debug(f'CFG GLOBAL CONFIG({self.cfg_local})')
        debug(f'CFG PROJECT: {self.project}')
        debug(f'CFG NAME:    {self.name}')

    def update_csvfilename(self, fname):
        """Update the csv filename for storing time data"""
        fname = self._replace_homepath(fname)
        self.docloc['csv']['filename'] = fname

    def get_filename_csv(self):
        """Get the csv filename where start and stop information is stored"""
        return abspath(join(self.csv_dir, self.csv_name))

    def str_cfg(self):
        """Return string containing configuration file contents"""
        return dumps(self.docloc)

    def wr_cfglocal(self):
        """Write config file"""
        with open(self.cfg_local, 'w', encoding='utf8') as ostrm:
            print(dumps(self.docloc), file=ostrm, end='')
            debug(f'  WROTE: {self.cfg_local}')

    def _replace_homepath(self, fname):
        fname = normpath(fname)
        home_str = expanduser('~')
        home_len = len(home_str)
        debug(f'UPDATE FNAME: {fname}')
        debug(f'UPDATE HOME:  {home_str}')
        return fname if fname[:home_len] != home_str else f'~{fname[home_len:]}'

    def _init_localdoc(self):
        doc = document()
        doc.add(comment("TimeTracker config file"))
        doc.add(nl())
        doc["title"] = "TimeTracker"

        # [csv]
        # format = "timetracker_dvklo.csv"
        csv_section = table()
        #csvdir.comment("Directory where the csv file is stored")
        csv_section.add("filename", normpath(relpath(self.get_filename_csv())))
        ##csv_section["csv_dir"].comment('Directory for the local config file')
        ##
        ### Adding the table to the document
        doc.add("csv", csv_section)

        return doc


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
