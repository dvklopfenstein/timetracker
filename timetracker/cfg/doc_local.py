"""Local project configuration parser for timetracking.

Uses https://github.com/python-poetry/tomlkit,
but will switch to tomllib in builtin to standard Python (starting 3.11)
in a version supported by cygwin, conda, and venv.

"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import dirname
from os.path import normpath
from collections import namedtuple
from glob import glob
from timetracker.cfg.utils import get_username
from timetracker.cfg.utils import get_abspath
from timetracker.cfg.utils import replace_envvar
from timetracker.cfg.tomutils import read_config
from timetracker.cfg.docutils import get_value


NTDOC = namedtuple('NtDoc', 'doc docproj')

def get_docproj(filename):
    """Get a DocProj object, given a global config filename"""
    ntcfg = read_config(filename)
    return DocProj(ntcfg.doc, filename) if ntcfg.doc else None

def get_ntdocproj(filename):
    """Get a DocProj object, given a global config filename"""
    ntcfg = read_config(filename)
    if ntcfg.doc is not None:
        return NTDOC(doc=ntcfg.doc, docproj=DocProj(ntcfg.doc, filename))
    return ntcfg

# pylint: disable=too-few-public-methods
class DocProj:
    """Local project configuration parser for timetracking"""

    CSVPAT = 'timetracker_PROJECT_$USER$.csv'

    def __init__(self, doc, filename):
        assert doc is not None
        assert type(doc).__name__ != 'RdCfg'
        assert filename is not None
        self.dircfg  = normpath(dirname(filename))
        self.dirproj = dirname(self.dircfg)
        #debug(pink(f'DocProj args filename {filename}'))
        self.project, self.csv_filename, self.global_config_filename, self.errors = \
            self._init_cfg_values(doc)
        self.dircsv = dirname(self.csv_filename) if self.csv_filename else None

    def get_abspath_dircsv(self):
        """Get the absolute pathname for doc['csv']['filename']"""
        if self.dircsv is not None and self.dirproj is not None:
            return get_abspath(self.dircsv, self.dirproj)
        return None


    def get_filename_csv(self, username=None, dirhome=None):
        """Get the csv filename by reading the cfg csv pattern and filling in"""
        username = get_username(username)
        return self._get_csvfilename_proj_user(username, dirhome)

    def get_filenames_csv(self, dirhome):
        """Get the csv filename by reading the cfg csv pattern and filling in"""
        fcsvpat = self._get_csvfilename_proj(dirhome)
        if fcsvpat is not None:
            globpat = replace_envvar(fcsvpat, '*')
            return glob(globpat)
        return None

    def _init_cfg_values(self, doc):
        """Get the config values from the local config as written"""
        ####print(doc)
        project = get_value(doc, 'project')
        ####print('VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV', project.value)
        ####print('VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVERR', project.error)
        csv_filename = get_value(doc, 'csv', 'filename')
        global_config_filename = get_value(doc, 'global_config', 'filename')
        return project.value, \
               csv_filename.value, \
               global_config_filename.value, \
               {'project': project.error,
                'csv_filename': csv_filename.error,
                'global_config_filename': global_config_filename.error}

    #def set_filename_csv(self, filename_str):
    #    """Write the config file, replacing [csv][filename] value"""
    #    filenamecfg = self.get_filename_cfg()
    #    if exists(filenamecfg):
    #        doc = TOMLFile(filenamecfg).read()
    #        doc['csv']['filename'] = filename_str
    #        self._wr_cfg(filenamecfg, doc)
    #        return
    #    raise RuntimeError(f"CAN NOT WRITE {filenamecfg}")


    #def reinit(self, project, dircsv, fcfg_global=None):
    #    """Update the cfg file, if needed"""
    #    fname = self.get_filename_cfg()
    #    assert exists(fname)   # checked in Cfg.reinit prior to calling
    #    doc = TOMLFile(fname).read()
    #    assert 'project' in doc
    #    assert 'csv' in doc
    #    assert 'filename' in doc['csv']
    #    proj_orig = doc.get('project')
    #    csv_orig = doc['csv'].get('filename')
    #    chgd = False
    #    if proj_orig != project:
    #        print(f'{fname} -> Changed `project` from {proj_orig} to {project}')
    #        doc['project'] = project
    #        chgd = True
    #    csv_new = self._ini_csv_filename(dircsv)
    #    if csv_orig != csv_new:
    #        print(f'{fname} -> Changed csv directory from {csv_orig} to {csv_new}')
    #        doc['csv']['filename'] = self._ini_csv_filename(dircsv)
    #        chgd = True
    #    if fcfg_global is not None:
    #        self._update_doc_globalcfgname(doc, fcfg_global)
    #    if chgd:
    #        TOMLFile(fname).write(doc)
    #    else:
    #        print(f'No changes needed to global config: {self.filename}')

    #def get_project_from_filename(self):
    #    """Get the default project name from the project directory filename"""
    #    return basename(self.dirproj)

    ##-------------------------------------------------------------
    def _get_csvfilename_proj_user(self, username, dirhome):
        """Read a config file and load it into a TOML document"""
        fcsvpat = self._get_csvfilename_proj(dirhome)
        if fcsvpat:
            return replace_envvar(fcsvpat, username) if '$' in fcsvpat else fcsvpat
        return None

    def _get_csvfilename_proj(self, dirhome):
        """Read a config file and load it into a TOML document"""
        if self.csv_filename and self.project:
            fpat = get_abspath(self.csv_filename, self.dirproj, dirhome)
            return fpat.replace('PROJECT', self.project)
        return None

    def _get_csv_filename(self, dirhome):
        """Read a config file and load it into a TOML document"""
        fcsvpat = self.csv_filename
        return get_abspath(fcsvpat, self.dirproj, dirhome) if fcsvpat is not None else None

    #@staticmethod
    #def _wr_cfg(fname, doc):
    #    """Write config file"""
    #    TOMLFile(fname).write(doc)
    #    # Use `~`, if it makes the path shorter
    #    ##fcsv = replace_homepath(doc['csv']['filename'])
    #    ##doc['csv']['filename'] = fcsv
    #    debug(pink(f'CfgProj _wr_cfg(...)  PROJ:     {doc["project"]}'))
    #    debug(pink(f"CfgProj _wr_cfg(...)  CSV:      {doc['csv']['filename']}"))
    #    debug(pink("CfgProj _wr_cfg(...)  GLOBAL    "
    #        f"{doc['global_config']['filename'] if 'global_config' in doc else 'NONE'}"))
    #    debug(pink(f'CfgProj _wr_cfg(...)  WROTE:    {fname}'))

    #def _rd_doc(self):
    #    """Read a config file and load it into a TOML document"""
    #    fin_cfglocal = self.get_filename_cfg()
    #    return TOMLFile(fin_cfglocal).read() if exists(fin_cfglocal) else None

    ##@staticmethod
    ##def _strdbg_cfg_global(doc):
    ##    return doc['global_config']['filename'] if 'global_config' in doc else 'NONE}


    #def _update_doc_globalcfgname(self, doc, fcfg_global):
    #    if 'global_config' not in doc:
    #        self._add_doc_globalcfgfname(doc, fcfg_global)
    #    elif 'filename' in doc['global_config']:
    #        if (cur := doc['global_config']['filename']) != fcfg_global:
    #            debug(pink(f'CfgProj WAS (fcfg_global={cur})'))
    #            doc['global_config']['filename'] = fcfg_global
    #            debug(pink(f'CfgProj NOW (fcfg_global={fcfg_global})'))
    #    else:
    #        doc['global_config']['filename'] = fcfg_global
    #        debug(pink(f'CfgProj SET (fcfg_global={fcfg_global})'))

    #@staticmethod
    #def _add_doc_globalcfgfname(doc, fcfg_global):
    #    # [global_config]
    #    # filename = "/home/uname/myglobal.cfg"
    #    section = table()
    #    #csvdir.comment("Directory where the csv file is stored")
    #    section.add("filename", fcfg_global)
    #    doc.add("global_config", section)
    #    debug(pink(f'CfgProj _add_doc_globalcfgfname(fcfg_global={fcfg_global})'))


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
