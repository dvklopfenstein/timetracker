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

from timetracker.cfg.starttime import Starttime
from timetracker.utils import pink
from timetracker.cfg.utils import get_username
from timetracker.cfg.utils import get_abspath
from timetracker.cfg.utils import get_relpath
from timetracker.cfg.utils import replace_envvar

# pylint: disable=fixme

class CfgProj:
    """Local project configuration parser for timetracking"""

    CSVPAT = 'timetracker_PROJECT_$USER$.csv'

    ####def __init__(self, filename, dircsv=None, project=None):
    def __init__(self, filename, project=None):
        self.filename = filename
        debug(pink(f'CfgProj args {int(exists(filename))} filename {filename}'))
        debug(f'CfgProj args . project  {project}')
        self.trksubdir = DIRTRK if filename is None else basename(dirname(filename))
        self.dircfg  = abspath(DIRTRK) if filename is None else normpath(dirname(filename))
        self.dirproj = dirname(self.dircfg)
        self.project = basename(self.dirproj) if project is None else project
        ####self.dircsv = self._get_dircsv() if dircsv is None else dircsv

    def get_filename_cfg(self):
        """Get the full filename of the local config file"""
        return join(self.dircfg, 'config')

    def get_filename_csv(self, username=None):
        """Read the local cfg to get the csv filename for storing time data"""
        username = get_username(username)
        fcsv = self._read_csv_from_cfgfile(username)
        if fcsv is not None:
            return fcsv
        return replace_envvar(self._get_dircsv_absname(), username)

    def set_filename_csv(self, filename_str):
        """Write the config file, replacing [csv][filename] value"""
        filenamecfg = self.get_filename_cfg()
        if exists(filenamecfg):
            doc = TOMLFile(filenamecfg).read()
            doc['csv']['filename'] = filename_str
            self._wrcfg(filenamecfg, doc)
            return
        raise RuntimeError(f"CAN NOT WRITE {filenamecfg}")

    def get_starttime_obj(self, username=None):
        """Get a Starttime instance"""
        username = get_username(username)
        project = self._read_project_from_cfgfile()
        return Starttime(self.dircfg, project, username)

    def write(self, force=False, quiet=False):
        """Write a new config file"""
        fname = self.get_filename_cfg()
        self._mk_dircfg(quiet)
        if not exists(fname):
            doc = self._get_doc_new()
            self._wr_cfg(fname, doc)
        elif force:
            doc = self._get_doc_new()
            self._wr_cfg(fname, doc)
            print(f'Overwrote {fname}')
        else:
            print(f'Use `force` to overwrite: {fname}')

    ####def str_cfg(self):
    ####    """Return string containing configuration file contents"""
    ####    return dumps(self._get_doc_new())

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

    def _read_cfgfile(self):
        """Read a config file and load it into a TOML document"""
        fin_cfglocal = self.get_filename_cfg()
        return TOMLFile(fin_cfglocal).read() if exists(fin_cfglocal) else None

    def _read_project_from_cfgfile(self):
        """Read a config file and load it into a TOML document"""
        doc = self._read_cfgfile()
        if doc is not None:
            return doc.get('project')  # , basename(dirname(dirname(fin_cfglocal))))
        return None

    def _read_csv_from_cfgfile(self, username):
        """Read a config file and load it into a TOML document"""
        doc = self._read_cfgfile()
        if doc is not None:
            fpat = get_abspath(doc['csv']['filename'], self.dirproj)
            ##fcsv_orig = join(dircsv, self.CSVPAT.replace('PROJECT', self.project))
            return replace_envvar(fpat, username) if '$' in fpat else fpat
        return None

    def _read_csvdir_from_cfgfile(self):
        """Read a config file and load it into a TOML document"""
        doc = self._read_cfgfile()
        if doc is not None:
            return get_abspath(dirname(doc['csv']['filename']), self.dirproj)
        return None

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

    def _get_dircsv(self):
        """Read the project cfg to get the csv dir name for storing time data"""
        fcsv = self._read_csvdir_from_cfgfile()
        ####debug(f'CCCCCCCCCC dircsv: {fcfg}')
        ####debug(f'CCCCCCCCCC dircsv: {fcsv}')
        if fcsv is not None:
            return dirname(fcsv)
        dircsv = get_abspath(DIRCSV, self.dirproj)
        ####debug(f'DDDDDDDDDD dircsv: {dircsv}')
        return dircsv

    def _get_dircsv_absname(self):
        dircsv = self._get_dircsv()
        ####fcsv_orig = join(dircsv, self.CSVPAT.replace('PROJECT', self.project))
        ####debug(f'BBBBBBBBBB {dircsv}')
        ####debug(f'BBBBBBBBBB {fcsv_orig}')
        ####return get_abspath(fcsv_orig, self.dirproj)
        return get_abspath(dircsv, self.dirproj)

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
        ##
        ### Adding the table to the document
        doc.add("csv", csv_section)
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
