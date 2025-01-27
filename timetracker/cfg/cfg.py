"""Configuration parser for timetracking.

Uses https://github.com/python-poetry/tomlkit,
but will switch to tomllib in builtin to standard Python (starting 3.11)
in a version supported by cygwin, conda, and venv.

"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import environ
from os import getcwd
from os.path import exists
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
from tomlkit import parse
from timetracker.cfg.utils import replace_envvar
from timetracker.cfg.utils import get_dirname_abs
from timetracker.cfg.utils import chk_isdir
from timetracker.cfg.utils import replace_homepath


class Cfg:
    """Configuration parser for timetracking"""
    # pylint: disable=too-few-public-methods

    DIR = './.timetracker'
    CSVPAT = 'timetracker_PROJECT_$USER$.csv'

    def __init__(self):
        self.cfg_global = expanduser('~/.timetrackerconfig')
        self.project = basename(getcwd())
        self.name = environ.get('USER', 'researcher')
        self.work_dir = abspath(self.DIR)
        self.dir_csv = '.'
        ##self.csv_name = join(
        ##    self.DIR,
        ##    self.CSVPAT.replace('PROJECT', self.project)
        self.docloc = self._init_localdoc()
        cfgloc = self.get_filename_cfglocal()
        debug(f'CFG LOCAL  CONFIG: exists({int(exists(self.cfg_global))}) -- {self.cfg_global}')
        debug(f'CFG GLOBAL CONFIG: exists({int(exists(cfgloc))}) -- {cfgloc}')
        debug(f'CFG PROJECT: {self.project}')
        debug(f'CFG NAME:    {self.name}')

    def read_filename_csv(self):
        """Read the local cfg to get the csv filename for storing time data"""
        doc = self._parse_local_cfg()
        assert doc is not None
        fpat = normpath(abspath(expanduser(doc['csv']['filename'])))
        return replace_envvar(fpat) if '$' in fpat else fpat

    def _parse_local_cfg(self):
        cfgtxt = self._read_local_cfg()
        ##debug(f'CFG: LOCALCFG({cfgtxt})')
        return parse(cfgtxt) if cfgtxt is not None else None

    def _read_local_cfg(self):
        fin = self.get_filename_cfglocal()
        with open(fin, encoding='utf8') as ifstrm:
            return ''.join(ifstrm.readlines())
        return None

    def get_filename_cfglocal(self):
        """Get the full filename of the local config file"""
        return join(self.work_dir, 'config')

    def get_filename_start(self):
        """Get the file storing the start time a person"""
        return join(self.work_dir, f'start_{self.project}_{self.name}.txt')

    def update_localini(self, project, csvdir):
        """Update the csv filename for storing time data"""
        self.project = project
        self.dir_csv = replace_homepath(csvdir)
        self.docloc['project'] = project
        fcsv = self._get_loc_filename()
        self.docloc['csv']['filename'] = fcsv
        debug(f'CFG:  CSVFILE exists({int(exists(fcsv))}) {fcsv}')

    def get_filename_csv(self):
        """Get the csv filename where start and stop information is stored"""
        fcsv = self.docloc['csv']['filename']
        debug(f'CFG:  CSVFILE exists({int(exists(fcsv))}) {fcsv}')
        return fcsv

    def str_cfg(self):
        """Return string containing configuration file contents"""
        return dumps(self.docloc)

    def wr_cfglocal(self):
        """Write config file"""
        fname = self.get_filename_cfglocal()
        chk_isdir(get_dirname_abs(self.docloc['csv']['filename']))
        with open(fname, 'w', encoding='utf8') as ostrm:
            print(dumps(self.docloc), file=ostrm, end='')
            debug(f'  WROTE: {fname}')

    def _get_loc_filename(self):
        return join(normpath(relpath(self.dir_csv)),
                    self.CSVPAT.replace('PROJECT', self.project))

    def _init_localdoc(self):
        doc = document()
        doc.add(comment("TimeTracker configuration file"))
        doc.add(nl())
        doc["project"] = self.project

        # [csv]
        # format = "timetracker_dvklo.csv"
        csv_section = table()
        #csvdir.comment("Directory where the csv file is stored")
        csv_section.add("filename", self._get_loc_filename())
        ##
        ### Adding the table to the document
        doc.add("csv", csv_section)

        return doc


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
