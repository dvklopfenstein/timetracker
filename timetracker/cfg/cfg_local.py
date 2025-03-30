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

    def __init__(self, filename, dirhome=None):
        self.filename = filename
        self.exists = exists(self.filename)
        debug(pink(f'CfgProj args {int(exists(filename))} filename {filename}'))
        if dirhome is not None:
            debug(pink(f'CfgProj args {int(exists(dirhome))} dirhome  {dirhome}'))
        self.trksubdir = DIRTRK if filename is None else basename(dirname(filename))
        self.dircfg  = abspath(DIRTRK) if filename is None else normpath(dirname(filename))
        self.dirproj = dirname(self.dircfg)
        self.dirhome = dirhome

    def get_filename_cfg(self):
        """Get the full filename of the local config file"""
        return join(self.dircfg, 'config')

    def get_filename_csv(self, username=None):
        """Get the csv filename by reading the cfg csv pattern and filling in"""
        username = get_username(username)
        fcsv = self._read_csv_from_cfgfile(username)
        return fcsv if fcsv is not None else None

    def get_project_csvs(self):
        """Get the csv filename by reading the cfg csv pattern and filling in"""
        fcsvpat = self._read_csvpat_from_cfgfile()
        if fcsvpat is not None:
            globpat = replace_envvar(fcsvpat, '*')
            return glob(globpat)
        return None

    @staticmethod
    def read_cfg(filename):
        """Read the given config file and return a doc object"""
        return TOMLFile(filename).read() if exists(filename) else None

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

    ##def write_file(self, project, dircsv='.', force=False):
    def wr_ini_file(self, project=None, dircsv=None, fcfg_global=None):
        """Write a new config file"""
        fname = self.get_filename_cfg()
        debug(f'CfgProj wr_ini_file {fname}')
        assert not exists(fname)
        #if exists(fname):
        #    return
        if not exists(self.dircfg):
            makedirs(self.dircfg, exist_ok=True)
        doc = self._get_doc_new(project)
        doc['csv']['filename'] = self._ini_csv_filename(dircsv)
        if fcfg_global is not None:
            self._add_doc_globalcfgfname(doc, fcfg_global)
        self._wr_cfg(fname, doc)
        print(f'Initialized timetracker directory: {self.dircfg}')
        ## if not exists(fname):
        ##    -- do the write ---
        ##elif force:
        ##    doc = self._get_doc_new(project)
        ##    doc['csv']['filename'] = join(dircsv, self.CSVPAT)
        ##    self._wr_cfg(fname, doc)
        ##    print(f'Overwrote {fname}')
        ##else:
        ##    print(f'Use `force` to overwrite: {fname}')

    def reinit(self, project, dircsv, fcfg_global=None):
        """Update the cfg file, if needed"""
        fname = self.get_filename_cfg()
        assert exists(fname)   # checked in Cfg.reinit prior to calling
        doc = TOMLFile(fname).read()
        assert 'project' in doc
        assert 'csv' in doc
        assert 'filename' in doc['csv']
        proj_orig = doc.get('project')
        csv_orig = doc['csv'].get('filename')
        chgd = False
        if proj_orig != project:
            print(f'{fname} -> Changed `project` from {proj_orig} to {project}')
            doc['project'] = project
            chgd = True
        csv_new = self._ini_csv_filename(dircsv)
        if csv_orig != csv_new:
            print(f'{fname} -> Changed csv directory from {csv_orig} to {csv_new}')
            doc['csv']['filename'] = self._ini_csv_filename(dircsv)
            chgd = True
        if fcfg_global is not None:
            raise RuntimeError('TIME TO IMPLEMENT ADDING/CHECKING Global config')
        if chgd:
            TOMLFile(fname).write(doc)
        else:
            print(f'No changes needed for {self.filename}')

    def read_doc(self):
        """Read the doc object"""
        return TOMLFile(self.filename).read() if exists(self.filename) else None

    def get_project_from_filename(self):
        """Get the default project name from the project directory filename"""
        return basename(self.dirproj)

    #-------------------------------------------------------------
    def _ini_csv_filename(self, dircsv):
        if dircsv is None:
            dircsv = '.'
        return join(dircsv, self.CSVPAT)

    def _rd_doc(self):
        """Read a config file and load it into a TOML document"""
        fin_cfglocal = self.get_filename_cfg()
        return TOMLFile(fin_cfglocal).read() if exists(fin_cfglocal) else None

    def _read_project_from_cfgfile(self):
        """Read a config file and load it into a TOML document"""
        doc = self._rd_doc()
        if doc is not None:
            return doc.get('project')  # , basename(dirname(dirname(fin_cfglocal))))
        return None

    def _read_csv_from_cfgfile(self, username):
        """Read a config file and load it into a TOML document"""
        fcsvpat = self._read_csvpat_from_cfgfile()
        if fcsvpat:
            return replace_envvar(fcsvpat, username) if '$' in fcsvpat else fcsvpat
        return None

    def _read_csvpat_from_cfgfile(self):
        """Read a config file and load it into a TOML document"""
        doc = self._rd_doc()
        if doc is not None:
            fpat = get_abspath(doc['csv']['filename'], self.dirproj, self.dirhome)
            fpat = fpat.replace('PROJECT', doc['project'])
            return fpat
        return None

    def _read_csvdir_from_cfgfile(self):
        """Read a config file and load it into a TOML document"""
        doc = self._rd_doc()
        if doc is not None:
            return get_abspath(dirname(doc['csv']['filename']), self.dirproj, self.dirhome)
        return None

    def _wr_cfg(self, fname, doc):
        """Write config file"""
        TOMLFile(fname).write(doc)
        # Use `~`, if it makes the path shorter
        ##fcsv = replace_homepath(doc['csv']['filename'])
        ##doc['csv']['filename'] = fcsv
        debug(pink(f'CfgProj _wr_cfg(...)  PROJ:     {doc["project"]}'))
        debug(pink(f"CfgProj _wr_cfg(...)  CSV:      {doc['csv']['filename']}"))
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

    def _get_doc_new(self, project):
        assert project is not None and isinstance(project, str)
        doc = document()
        doc.add(comment("TimeTracker project configuration file"))
        doc.add(nl())
        doc["project"] = project

        # [csv]
        # format = "timetracker_dvklo.csv"
        csv_section = table()
        #csvdir.comment("Directory where the csv file is stored")
        csvpat = self.CSVPAT.replace('PROJECT', project)
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

    @staticmethod
    def _add_doc_globalcfgfname(doc, fcfg_global):
        # [global_config]
        # filename = "/home/uname/myglobal.cfg"
        section = table()
        #csvdir.comment("Directory where the csv file is stored")
        section.add("filename", fcfg_global)
        doc.add("global_config", section)

    #-------------------------------------------------------------
    def get_desc(self, note=' set'):
        """Get a string describing the state of an instance of the CfgProj"""
        # pylint: disable=line-too-long
        #### f'CfgProj {note} . dircsv   {self.dircsv}\n'
        return (
            f'CfgProj {note} . trksdir  {self.trksubdir}\n'
            f'CfgProj {note} {int(exists(self.dircfg))} dircfg   {self.dircfg}\n'
            f'CfgProj {note} {int(exists(self.dirproj))} dirproj  {self.dirproj}\n'
            f'CfgProj {note} {int(exists(self.get_filename_csv()))} fname csv   {self.get_filename_csv()}\n'
            f'CfgProj {note} {int(exists(self.get_filename_cfg()))} fname cfg   {self.get_filename_cfg()}')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
