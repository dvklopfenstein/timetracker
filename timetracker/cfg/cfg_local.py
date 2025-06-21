"""Local project configuration parser for timetracking.

Uses https://github.com/python-poetry/tomlkit,
but will switch to tomllib in builtin to standard Python (starting 3.11)
in a version supported by cygwin, conda, and venv.

"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

import os
import os.path as op
from os.path import exists
from logging import debug
from collections import namedtuple

import tomlkit
from tomlkit.toml_file import TOMLFile

from timetracker.consts import DIRTRK
from timetracker.consts import DIRCSV

from timetracker.cfg.doc_local import get_docproj
from timetracker.cfg.doc_local import get_ntdocproj
from timetracker.cfg.tomutils import write_config
from timetracker.cfg.utils import get_abspath
from timetracker.cfg.utils import get_filename_globalcfg
#from timetracker.cfg.utils import get_relpath
#from timetracker.cfg.utils import replace_envvar


class CfgProj:
    """Local project configuration parser for timetracking"""

    CSVPAT = 'timetracker_PROJECT_$USER$.csv'
    NTFILE = namedtuple('NtFile', 'filename error')

    def __init__(self, filename):
        assert filename is not None
        self.filename = filename
        debug('CfgProj args %d filename %s', exists(filename), filename)
        dnam = op.dirname
        self.trksubdir = DIRTRK if filename is None else op.basename(dnam(filename))
        self.dircfg  = op.abspath(DIRTRK) if filename is None else op.normpath(dnam(filename))
        self.dirproj = dnam(self.dircfg)

    def file_exists(self):
        """Return True if config file exists and False otherwise"""
        return exists(self.filename)

    def get_filename_cfg(self):
        """Get the full filename of the local config file"""
        return op.join(self.dircfg, 'config')

    def get_filename_csv(self, username=None, dirhome=None):
        """Get the csv filename by reading the cfg csv pattern and filling in"""
        if (docproj := get_docproj(self.filename)):
            return docproj.get_filename_csv(username, dirhome)
        return None

    def get_filenames_csv(self, dirhome=None):
        """Get all csv filenames by reading the cfg csv pattern and globbing `*` username"""
        if (docproj := get_docproj(self.filename)):
            return docproj.get_filenames_csv(dirhome)
        return None

    def set_filename_csv(self, filename_str):
        """Write the config file, replacing [csv][filename] value"""
        filenamecfg = self.get_filename_cfg()
        if exists(filenamecfg):
            doc = TOMLFile(filenamecfg).read()
            doc['csv']['filename'] = filename_str
            return self._wr_cfg(filenamecfg, doc)
        raise RuntimeError(f"CAN NOT WRITE {filenamecfg}")

    def get_starttime_obj(self, username):
        """Get a Starttime instance"""
        if (docproj := get_docproj(self.filename)):
            return docproj.get_startobj(username)
        return None

    def timer_started(self, docproj, username):
        """Return True if the timer is started, False if not"""
        if docproj and (startobj := docproj.get_startobj(username)):
            return startobj.started()
        return False

    def wr_ini_file(self, project=None, dircsv=None, fcfg_global=None):
        """Write a new config file"""
        fname = self.get_filename_cfg()
        assert not exists(fname)
        if not exists(self.dircfg):
            os.makedirs(self.dircfg, exist_ok=True)
        if dircsv is None:
            dircsv = '.'
        doc = self._get_new_doc(project, dircsv)
        if fcfg_global is not None:
            self._add_doc_globalcfgfname(doc, fcfg_global)
        return self.NTFILE(filename=fname, error=self._wr_cfg(fname, doc))

    def wr_gitignore(self):
        """Add .gitignore file in .timetracker/ directory"""
        error = None
        fname = op.join(self.dircfg, '.gitignore')
        try:
            fptr = open(fname, 'w', encoding='utf-8')
        except (PermissionError, OSError) as err:
            error = err
        else:
            with fptr:
                fptr.write('start_*.txt')
        return self.NTFILE(filename=fname, error=error)

    def reinit(self, project, dircsv, fcfg_global=None, ntdoc=None):
        """Update the cfg file, if needed"""
        fname = self.get_filename_cfg()
        assert exists(fname)   # checked in Cfg.reinit prior to calling
        if ntdoc is None:
            ntdoc = get_ntdocproj(self.filename)
        assert ntdoc.doc is not None
        docproj = ntdoc.docproj
        assert docproj.project is not None
        assert docproj.csv_filename is not None
        chgd = False
        doc = ntdoc.doc
        if docproj.project != project:
            print(f'{fname} -> Changed `project` from {docproj.project} to {project}')
            doc['project'] = project
            chgd = True
        if docproj.csv_filename != (csv_new := self._assemble_csv_filepat(dircsv, doc['project'])):
            dnam = op.dirname
            print('In local project configuration file, changed csv directory:\n'
                  f'   local cfg:  {fname}\n'
                  f'      csvdir WAS: {dnam(docproj.csv_filename)}\n'
                  f'      csvdir NOW: {dnam(csv_new)}')
            doc['csv']['filename'] = csv_new
            chgd = True
        if fcfg_global is not None and docproj.global_config_filename != fcfg_global:
            fcfgg_orig = get_filename_globalcfg(fcfg_doc=docproj.global_config_filename)
            print(f'{fname} -> Changed the global config filename\n'
                  f'        from: "{fcfgg_orig}"\n'
                  f'        to:   "{fcfg_global}"')
            self._update_doc_globalcfgname(doc, fcfg_global)
            chgd = True
        if chgd:
            TOMLFile(fname).write(doc)
        else:
            print(f'No changes needed to local config: {self.filename}')

    def get_project_from_filename(self):
        """Get the default project name from the project directory filename"""
        return op.basename(self.dirproj)

    #-------------------------------------------------------------
    def _assemble_csv_filepat(self, dircsv, project):
        if dircsv is None or dircsv == '':
            dircsv = '.'
        return op.join(dircsv, self.CSVPAT.replace('PROJECT', project))

    @staticmethod
    def _wr_cfg(fname, doc):
        """Write config file"""
        ret = write_config(fname, doc)
        # Use `~`, if it makes the path shorter
        debug('CfgProj _wr_cfg(...)  PROJ:     %s', doc["project"])
        debug("CfgProj _wr_cfg(...)  CSV:      %s", doc['csv']['filename'])
        debug("CfgProj _wr_cfg(...)  GLOBAL    %s",
              doc['global_config']['filename'] if 'global_config' in doc else 'NONE')
        debug('CfgProj _wr_cfg(...)  WROTE:    %s', fname)
        return ret

    def _rd_doc(self):
        """Read a config file and load it into a TOML doc"""
        fin_cfglocal = self.get_filename_cfg()
        return TOMLFile(fin_cfglocal).read() if exists(fin_cfglocal) else None

    #@staticmethod
    #def _strdbg_cfg_global(doc):
    #    return doc['global_config']['filename'] if 'global_config' in doc else 'NONE}

    def _get_dircsv(self, dirhome):
        """Read the project cfg to get the csv dir name for storing time data"""
        ##fcsv = self._read_csvdir_from_cfgfile(dirhome)
        ##if fcsv is not None:
        ##    return op.dirname(fcsv)
        dircsv = get_abspath(DIRCSV, self.dirproj, dirhome)
        return dircsv

    ##def _get_dircsv_absname(self, dirhome):
    ##    dircsv = self._get_dircsv(dirhome)
    ##    return get_abspath(dircsv, self.dirproj, dirhome)

    ##def _get_dircsv_relname(self, dirhome):
    ##    fcsv_abs = self._get_dircsv_absname(dirhome)
    ##    return get_relpath(fcsv_abs, self.dirproj)

    ##def _get_new_doc(self, project, dircsv, dirhome):
    def _get_new_doc(self, project, dircsv):
        assert project is not None and isinstance(project, str)
        #assert dircsv
        debug('TODO: dircsv=%s', dircsv)
        doc = tomlkit.document()
        doc.add(tomlkit.comment("TimeTracker project configuration file"))
        doc.add(tomlkit.nl())
        doc["project"] = project

        # [csv]
        # format = "timetracker_architecting_bez.csv"
        csv_section = tomlkit.table()
        #csvdir.comment("Directory where the csv file is stored")
        ##csvpat = self.CSVPAT.replace('PROJECT', project)
        ##csv_section.add("filename", op.join(self._get_dircsv_relname(dirhome), csvpat))
        csv_section.add("filename", self._assemble_csv_filepat(dircsv, project))
        doc.add("csv", csv_section)
        return doc

    def _update_doc_globalcfgname(self, doc, fcfg_global):
        if 'global_config' not in doc:
            self._add_doc_globalcfgfname(doc, fcfg_global)
        elif 'filename' in doc['global_config']:
            if (cur := doc['global_config']['filename']) != fcfg_global:
                debug('CfgProj WAS (fcfg_global=%s', cur)
                doc['global_config']['filename'] = fcfg_global
                debug('CfgProj NOW (fcfg_global=%s', fcfg_global)
        else:
            doc['global_config']['filename'] = fcfg_global
            debug('CfgProj SET (fcfg_global=%s)', fcfg_global)

    @staticmethod
    def _add_doc_globalcfgfname(doc, fcfg_global):
        # [global_config]
        # filename = "/home/uname/myglobal.cfg"
        section = tomlkit.table()
        #csvdir.comment("Directory where the csv file is stored")
        section.add("filename", fcfg_global)
        doc.add("global_config", section)
        debug('CfgProj _add_doc_globalcfgfname(fcfg_global=%s)', fcfg_global)

    #-------------------------------------------------------------
    def get_desc(self, note=' set'):
        """Get a string describing the state of an instance of the CfgProj"""
        # pylint: disable=line-too-long
        docproj = get_docproj(self.filename)
        fcsv = docproj.csv_filename if docproj else None
        assert fcsv is not None, self.filename
        return (
            f'CfgProj {note} . trksdir  {self.trksubdir}\n'
            f'CfgProj {note} {int(exists(self.dircfg))} dircfg   {self.dircfg}\n'
            f'CfgProj {note} {int(exists(self.dirproj))} dirproj  {self.dirproj}\n'
            f'CfgProj {note} {int(exists(fcsv))} fname csv   {fcsv}\n'
            f'CfgProj {note} {int(exists(self.get_filename_cfg()))} fname cfg   {self.get_filename_cfg()}')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
