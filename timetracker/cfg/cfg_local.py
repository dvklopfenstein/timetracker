"""Local project configuration parser for timetracking.

Uses https://github.com/python-poetry/tomlkit,
but will switch to tomllib in builtin to standard Python (starting 3.11)
in a version supported by cygwin, conda, and venv.

"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

##from os import remove
from os import makedirs
from os.path import exists
from os.path import basename
from os.path import join
from os.path import abspath
##from os.path import relpath
from os.path import dirname
from os.path import normpath
from logging import debug
from glob import glob

from tomlkit import comment
from tomlkit import document
from tomlkit import nl
from tomlkit import table
from tomlkit.toml_file import TOMLFile

from timetracker.consts import DIRTRK
from timetracker.consts import DIRCSV

##from timetracker.cfg.utils import replace_homepath
##from timetracker.cfg.utils import parse_cfg
##from timetracker.cfg.utils import chk_isdir
##from timetracker.cfg.utils import get_dirname_abs

from timetracker.starttime import Starttime
from timetracker.utils import pink
from timetracker.cfg.utils import get_username
from timetracker.cfg.utils import get_abspath
from timetracker.cfg.utils import get_relpath
from timetracker.cfg.utils import replace_envvar

# pylint: disable=fixme

class CfgProj:
    """Local project configuration parser for timetracking"""

    CSVPAT = 'timetracker_PROJECT_$USER$.csv'

    def __init__(self, filename, project=None, dirhome=None):
        self.filename = filename
        debug(pink(f'CfgProj args {int(exists(filename))} filename {filename}'))
        if dirhome is not None:
            debug(pink(f'CfgProj args {int(exists(dirhome))} dirhome  {dirhome}'))
        debug(f'CfgProj args . project({project})')
        self.trksubdir = DIRTRK if filename is None else basename(dirname(filename))
        self.dircfg  = abspath(DIRTRK) if filename is None else normpath(dirname(filename))
        self.dirproj = dirname(self.dircfg)
        self.project = basename(self.dirproj) if project is None else project
        self.dirhome = dirhome
        ####self.dircsv = self._get_dircsv() if dircsv is None else dircsv

    def get_filename_cfg(self):
        """Get the full filename of the local config file"""
        return join(self.dircfg, 'config')

    def get_filename_csv(self, username=None):
        """Get the csv filename by reading the cfg csv pattern and filling in"""
        username = get_username(username)
        fcsv = self._read_csv_from_cfgfile(username)
        ####if fcsv is not None:
        ####    return fcsv
        ####return replace_envvar(self._get_dircsv_absname(), username)
        ####return None
        return fcsv if fcsv is not None else None

    def get_project_csvs(self):
        """Get the csv filename by reading the cfg csv pattern and filling in"""
        fcsvpat = self._read_csvpat_from_cfgfile()
        if fcsvpat is not None:
            globpat = replace_envvar(fcsvpat, '*')
            return glob(globpat)
        return None

    def set_filename_csv(self, filename_str):
        """Write the config file, replacing [csv][filename] value"""
        filenamecfg = self.get_filename_cfg()
        if exists(filenamecfg):
            doc = TOMLFile(filenamecfg).read()
            doc['csv']['filename'] = filename_str
            self._wr_cfg(filenamecfg, doc)
            return
        raise RuntimeError(f"CAN NOT WRITE {filenamecfg}")

    def get_starttime_obj(self, username):
        """Get a Starttime instance"""
        username = get_username(username)
        project = self._read_project_from_cfgfile()
        return Starttime(self.dircfg, project, username)

    def write_file(self, dircsv='.', force=False, quiet=False):
        """Write a new config file"""
        if dircsv is None:
            dircsv = '.'
        fname = self.get_filename_cfg()
        self._mk_dircfg(quiet)
        if not exists(fname):
            doc = self._get_doc_new()
            doc['csv']['filename'] = join(dircsv, self.CSVPAT)
            self._wr_cfg(fname, doc)
        elif force:
            doc = self._get_doc_new()
            doc['csv']['filename'] = join(dircsv, self.CSVPAT)
            self._wr_cfg(fname, doc)
            if not quiet:
                print(f'Overwrote {fname}')
        else:
            if not quiet:
                print(f'Use `force` to overwrite: {fname}')

    def read_doc(self):
        """Read a config file and load it into a TOML document"""
        fin_cfglocal = self.get_filename_cfg()
        return TOMLFile(fin_cfglocal).read() if exists(fin_cfglocal) else None

    #-------------------------------------------------------------
    def _mk_dircfg(self, quiet=False):
        """Makes a `.timetracker/` working directory, if needed; The project cfg is stored here"""
        dircfg = self.dircfg
        debug(f'mk_dircfg({dircfg})')
        if not exists(dircfg):
            makedirs(dircfg, exist_ok=True)
            absdir = abspath(dircfg)
            if not quiet:
                print(f'Initialized timetracker directory: {absdir}')

    def _read_project_from_cfgfile(self):
        """Read a config file and load it into a TOML document"""
        doc = self.read_doc()
        if doc is not None:
            return doc.get('project')  # , basename(dirname(dirname(fin_cfglocal))))
        return None

    def _read_csv_from_cfgfile(self, username):
        """Read a config file and load it into a TOML document"""
        ####doc = self.read_doc()
        ####if doc is not None:
        ####    fpat = get_abspath(doc['csv']['filename'], self.dirproj, self.dirhome)
        ####    fpat = fpat.replace('PROJECT', self.project)
        fcsvpat = self._read_csvpat_from_cfgfile()
        if fcsvpat:
            return replace_envvar(fcsvpat, username) if '$' in fcsvpat else fcsvpat
        return None

    def _read_csvpat_from_cfgfile(self):
        """Read a config file and load it into a TOML document"""
        doc = self.read_doc()
        if doc is not None:
            fpat = get_abspath(doc['csv']['filename'], self.dirproj, self.dirhome)
            fpat = fpat.replace('PROJECT', self.project)
            return fpat
        return None

    def _read_csvdir_from_cfgfile(self):
        """Read a config file and load it into a TOML document"""
        doc = self.read_doc()
        if doc is not None:
            return get_abspath(dirname(doc['csv']['filename']), self.dirproj, self.dirhome)
        return None

    def _wr_cfg(self, fname, doc):
        """Write config file"""
        TOMLFile(fname).write(doc)
        # Use `~`, if it makes the path shorter
        ##fcsv = replace_homepath(doc['csv']['filename'])
        ##doc['csv']['filename'] = fcsv
        fcsv = doc['csv']['filename']
        debug(pink(f'CfgProj _wr_cfg(...)  CSV:      {fcsv}'))
        debug(pink(f'CfgProj _wr_cfg(...)  WROTE:    {fname}'))

    def _get_dircsv(self):
        """Read the project cfg to get the csv dir name for storing time data"""
        fcsv = self._read_csvdir_from_cfgfile()
        if fcsv is not None:
            return dirname(fcsv)
        dircsv = get_abspath(DIRCSV, self.dirproj, self.dirhome)
        return dircsv

    def _get_dircsv_absname(self):
        dircsv = self._get_dircsv()
        return get_abspath(dircsv, self.dirproj, self.dirhome)

    def _get_dircsv_relname(self):
        fcsv_abs = self._get_dircsv_absname()
        return get_relpath(fcsv_abs, self.dirproj)

    def _get_doc_new(self):
        doc = document()
        doc.add(comment("TimeTracker project configuration file"))
        doc.add(nl())
        doc["project"] = self.project

        # [csv]
        # format = "timetracker_dvklo.csv"
        csv_section = table()
        #csvdir.comment("Directory where the csv file is stored")
        csvpat = self.CSVPAT.replace('PROJECT', self.project)
        csv_section.add("filename", join(self._get_dircsv_relname(), csvpat))
        doc.add("csv", csv_section)

        # TODO: [display]
        # format = "24-hour"
        # --or--
        # format = "12-hour"
        # --or use datetime format codes--
        # # https://docs.python.org/3/library/datetime.html#format-codes
        # format = '%a %p %Y-%m-%d %H:%M:%S'
        return doc

    #-------------------------------------------------------------
    def get_desc(self, note=' set'):
        """Get a string describing the state of an instance of the CfgProj"""
        # pylint: disable=line-too-long
        #### f'CfgProj {note} . dircsv   {self.dircsv}\n'
        return (
            f'CfgProj {note} . trksdir  {self.trksubdir}\n'
            f'CfgProj {note} {int(exists(self.dircfg))} dircfg   {self.dircfg}\n'
            f'CfgProj {note} . project  {self.project}\n'
            f'CfgProj {note} {int(exists(self.dirproj))} dirproj  {self.dirproj}\n'
            f'CfgProj {note} {int(exists(self.get_filename_csv()))} fname csv   {self.get_filename_csv()}\n'
            f'CfgProj {note} {int(exists(self.get_filename_cfg()))} fname cfg   {self.get_filename_cfg()}')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
