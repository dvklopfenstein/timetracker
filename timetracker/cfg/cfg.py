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
from timetracker.cfg.utils import replace_envvar
from timetracker.cfg.utils import replace_homepath
from timetracker.cfg.utils import parse_cfg
from timetracker.cfg.utils import chk_isdir
from timetracker.cfg.utils import get_dirname_abs


class Cfg:
    """Configuration parser for timetracking"""

    DIR = './.timetracker'
    CSVPAT = 'timetracker_PROJECT_$USER$.csv'

    def __init__(self):
        self.project = basename(getcwd())
        self.name = environ.get('USER', 'researcher')
        self.work_dir = abspath(self.DIR)
        self.dir_csv = '.'
        ##self.csv_name = join(
        ##    self.DIR,
        ##    self.CSVPAT.replace('PROJECT', self.project)
        self.doc = self._init_doclocal()
        cfgloc = self.get_filename_cfglocal()
        debug(f'CFG LOCAL  CONFIG: exists({int(exists(cfgloc))}) -- {cfgloc}')
        debug(f'CFG PROJECT: {self.project}')
        debug(f'CFG NAME:    {self.name}')

    def get_filename_cfglocal(self):
        """Get the full filename of the local config file"""
        return normpath(abspath(join(self.work_dir, 'config')))

    def get_filename_csv(self):
        """Read the local cfg to get the csv filename for storing time data"""
        fcfg = self.get_filename_cfglocal()
        doc = parse_cfg(fcfg, "CFG LOCAL")
        assert doc is not None
        fpat = normpath(abspath(expanduser(doc['csv']['filename'])))
        return replace_envvar(fpat) if '$' in fpat else fpat

    def get_filename_start(self):
        """Get the file storing the start time a person"""
        return join(self.work_dir, f'start_{self.project}_{self.name}.txt')

    def wr_cfg(self):
        """Write config file"""
        fname = self.get_filename_cfglocal()
        chk_isdir(get_dirname_abs(self.doc['csv']['filename']))
        with open(fname, 'w', encoding='utf8') as ostrm:
            print(self.str_cfg(), file=ostrm, end='')
            debug(f'  WROTE: {fname}')
        return dumps(self.doc)

    def update_localini(self, project, csvdir):
        """Update the csv filename for storing time data"""
        self.project = project
        self.dir_csv = replace_homepath(csvdir)
        self.doc['project'] = project
        fcsv = self._get_loc_filename()
        self.doc['csv']['filename'] = fcsv
        debug(f'CFG:  CSVFILE exists({int(exists(fcsv))}) {fcsv}')

    def str_cfg(self):
        """Return string containing configuration file contents"""
        return dumps(self.doc)

    #-------------------------------------------------------------
    def _get_loc_filename(self):
        return join(normpath(relpath(self.dir_csv)),
                    self.CSVPAT.replace('PROJECT', self.project))

    def _init_docglobal(self):
        doc = document()
        doc.add(comment("TimeTracker global configuration file"))
        doc.add(nl())
        doc["projects"] = []
        return doc

    def _init_doclocal(self):
        doc = document()
        doc.add(comment("TimeTracker project configuration file"))
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

    ##def _get_filename_csv(self):
    ##    """Get the csv filename where start and stop information is stored"""
    ##    fcsv = self.doc['csv']['filename']
    ##    debug(f'CFG:  CSVFILE exists({int(exists(fcsv))}) {fcsv}')
    ##    return fcsv

# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
