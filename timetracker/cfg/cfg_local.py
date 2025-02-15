"""Local project configuration parser for timetracking.

Uses https://github.com/python-poetry/tomlkit,
but will switch to tomllib in builtin to standard Python (starting 3.11)
in a version supported by cygwin, conda, and venv.

"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import remove
from os import makedirs
from os.path import exists
from os.path import basename
from os.path import join
from os.path import abspath
##from os.path import relpath
from os.path import dirname
from os.path import normpath
from logging import debug

from tomlkit import comment
from tomlkit import document
from tomlkit import nl
from tomlkit import table
from tomlkit import dumps
from tomlkit.toml_file import TOMLFile

from timetracker.consts import DIRTRK
from timetracker.consts import DIRCSV

##from timetracker.cfg.utils import replace_homepath
##from timetracker.cfg.utils import parse_cfg
##from timetracker.cfg.utils import chk_isdir
##from timetracker.cfg.utils import get_dirname_abs

from timetracker.cfg.utils import get_username
from timetracker.cfg.utils import get_abspath
from timetracker.cfg.utils import get_relpath
from timetracker.cfg.utils import replace_envvar
from timetracker.hms import hms_from_startfile
from timetracker.hms import read_starttime as hms_read_starttime

# pylint: disable=fixme

class CfgProj:
    """Local project configuration parser for timetracking"""

    CSVPAT = 'timetracker_PROJECT_$USER$.csv'

    def __init__(self, filename=None, dircsv=None, project=None, name=None):
        self.filename = filename
        debug(f'CfgProj args {int(exists(filename))} filename {filename}')
        debug(f'CfgProj args . project  {project}')
        debug(f'CfgProj args . name     {name}')
        self.trksubdir = DIRTRK if filename is None else basename(dirname(filename))
        self.dircfg  = abspath(DIRTRK) if filename is None else normpath(dirname(filename))
        self.dirproj = dirname(self.dircfg)
        self.project = basename(self.dirproj) if project is None else project
        self.name = get_username(name) if name is None else name
        self.dircsv = self._init_dircsv() if dircsv is None else dircsv
        debug(f'CfgProj  set . trksdir  {self.trksubdir}')
        debug(f'CfgProj  set {int(exists(self.dircfg))} dircfg   {self.dircfg}')
        debug(f'CfgProj  set . project  {self.project}')
        debug(f'CfgProj  set . name     {self.name}')
        debug(f'CfgProj  set {int(exists(self.dircsv))} dircsv   {self.dircsv}')
        debug(f'CfgProj  set . fname cfg   {self.get_filename_cfglocal()}')
        # pylint: disable=line-too-long
        debug(f'CfgProj  set {int(exists(self.get_filename_cfg()))} fname cfg   {self.get_filename_cfg()}')
        debug(f'CfgProj  set {int(exists(self.get_filename_csv()))} fname csv   {self.get_filename_csv()}')
        debug(f'CfgProj  set {int(exists(self.get_filename_start()))} fname start {self.get_filename_start()}')

    def get_filename_cfglocal(self):
        """Get the full filename of the local config file"""
        # TODO: Invocrrect in tmp trr start
        return get_relpath(self.get_filename_cfg(), self.dirproj)

    def get_filename_cfg(self):
        """Get the full filename of the local config file"""
        return join(self.dircfg, 'config')

    def get_filename_csv(self):
        """Read the local cfg to get the csv filename for storing time data"""
        fcfg = self.get_filename_cfg()
        fcsv = self._read_csv_from_cfgfile(fcfg)
        return fcsv if fcsv is not None else replace_envvar(self._get_csv_absname())

    def _init_dircsv(self):
        """Read the local cfg to get the csv filename for storing time data"""
        fcfg = self.get_filename_cfg()
        fcsv = self._read_csv_from_cfgfile(fcfg)
        ####debug(f'CCCCCCCCCC dircsv: {fcfg}')
        ####debug(f'CCCCCCCCCC dircsv: {fcsv}')
        if fcsv is not None:
            return dirname(fcsv)
        dircsv = get_abspath(DIRCSV, self.dirproj)
        ####debug(f'DDDDDDDDDD dircsv: {dircsv}')
        return dircsv

    def get_filename_start(self):
        """Get the file storing the start time a person"""
        fstart = join(self.dircfg, f'start_{self.project}_{self.name}.txt')
        ####debug(f'CFG LOCAL: STARTFILE exists({int(exists(fstart))}) {relpath(fstart)}')
        return fstart

    def read_starttime(self):
        """Read the start time file"""
        fname = self.get_filename_start()
        return hms_read_starttime(fname)

    def wr_cfg_new(self):
        """Write a new config file"""
        fname = self.get_filename_cfg()
        doc = self._get_doc_new()
        self._wr_cfg(fname, doc)

    def _wr_cfg(self, fname, doc):
        """Write config file"""
        ##chk_isdir(get_dirname_abs(doc['csv']['filename']), "doc['csv']['filename']")
        debug(doc.as_string())
        TOMLFile(fname).write(doc)
        # Use `~`, if it makes the path shorter
        ##fcsv = replace_homepath(doc['csv']['filename'])
        ##doc['csv']['filename'] = fcsv
        fcsv = doc['csv']['filename']
        debug(f'CfgProj _wr_cfg(...)  CSV:      {fcsv}')
        debug(f'CfgProj _wr_cfg(...)  WROTE:    {fname}')

    def _read_csv_from_cfgfile(self, fin_cfglocal):
        """Read a config file and load it into a TOML document"""
        doc = TOMLFile(fin_cfglocal).read() if exists(fin_cfglocal) else None
        if doc is not None:
            fpat = get_abspath(doc['csv']['filename'], self.dirproj)
            return replace_envvar(fpat) if '$' in fpat else fpat
        return None

    ####def update_localini(self, project, csvdir):
    ####    """Update the csv filename for storing time data"""
    ####    if project is not None:
    ####        self.project = project
    ####    if csvdir is not None:
    ####        self.dircsv = replace_homepath(csvdir)
    ####    self.doc['project'] = self.project
    ####    fcsv = self._get_csv_relname()
    ####    self.doc['csv']['filename'] = fcsv
    ####    debug(f'CFG:  CSVFILE exists({int(exists(fcsv))}) {fcsv}')

    def str_cfg(self):
        """Return string containing configuration file contents"""
        return dumps(self._get_doc_new())

    def prt_elapsed(self):
        """Print elapsed time if timer is started"""
        fin_start = self.get_filename_start()
        # Print elapsed time, if timer was started
        if exists(fin_start):
            hms = hms_from_startfile(fin_start)
            print(f'\nTimer running: {hms} H:M:S '
                  f"elapsed time for '{self.project}' ID={self.name}")

    def rm_starttime(self):
        """Remove the starttime file, thus resetting the timer"""
        fstart = self.get_filename_start()
        if exists(fstart):
            remove(fstart)

    def mk_dircfg(self, quiet=False):
        """Initialize `.timetracker/` project working directory"""
        dircfg = self.dircfg
        debug(f'mk_dircfg({dircfg})')
        if not exists(dircfg):
            makedirs(dircfg, exist_ok=True)
            absdir = abspath(dircfg)
            if not quiet:
                print(f'Initialized timetracker directory: {absdir}')

    #-------------------------------------------------------------
    def __str__(self):
        return (
        f'CfgProj set  trksdir {self.trksubdir}\n'
        f'CfgProj set  dircfg  {self.dircfg}\n'
        f'CfgProj set  project {self.project}\n'
        f'CfgProj set  name    {self.name}\n'
        f'CfgProj set  dircsv  {self.dircsv}')

    def _get_csv_absname(self):
        fcsv_orig = join(self.dircsv, self.CSVPAT.replace('PROJECT', self.project))
        ####debug(f'BBBBBBBBBB {self.dircsv}')
        ####debug(f'BBBBBBBBBB {fcsv_orig}')
        return get_abspath(fcsv_orig, self.dirproj)

    def _get_csv_relname(self):
        fcsv_abs = self._get_csv_absname()
        return get_relpath(fcsv_abs, self.dirproj)

    @staticmethod
    def _init_docglobal():
        doc = document()
        doc.add(comment("TimeTracker global configuration file"))
        doc.add(nl())
        doc["projects"] = []
        return doc

    def _get_doc_new(self):
        doc = document()
        doc.add(comment("TimeTracker project configuration file"))
        doc.add(nl())
        doc["project"] = self.project

        # [csv]
        # format = "timetracker_dvklo.csv"
        csv_section = table()
        #csvdir.comment("Directory where the csv file is stored")
        csv_section.add("filename", self._get_csv_relname())
        ##
        ### Adding the table to the document
        doc.add("csv", csv_section)
        return doc


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
