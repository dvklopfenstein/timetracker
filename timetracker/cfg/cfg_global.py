"""Global configuration parser for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

import os.path as op
from os.path import exists
from logging import debug
from collections import namedtuple

import tomlkit
from tomlkit.toml_file import TOMLFile

from timetracker.cfg.tomutils import read_config
from timetracker.cfg.tomutils import write_config
from timetracker.cfg.utils import has_homedir
from timetracker.cfg.utils import get_filename_globalcfg


def get_cfgglobal(fcfg_explicit=None, dirhome=None, fcfg_doc=None):
    """Get a global configuration object"""
    return CfgGlobal(get_filename_globalcfg(dirhome, fcfg_explicit, fcfg_doc))


class CfgGlobal:
    """Global configuration parser for timetracking"""

    NTWRCFG = namedtuple('WrCfg', 'doc error')

    def __init__(self, filename):
        self.filename = filename
        debug('CfgGlobal CONFIG: exists(%d) -- %s', exists(filename), filename)

    def get_projects(self):
        """Get the projects managed by timetracker"""
        ntcfg = read_config(self.filename)
        if ntcfg.doc:
            return ntcfg.doc.get('projects')
        return None

    def set_projects(self, projects):
        """Set the list of projects to the given list of projects"""
        ntcfg = read_config(self.filename)
        if ntcfg.doc:
            arr = ntcfg.doc['projects']
            arr.clear()
            for elem in projects:
                arr.add_line(elem)
            self.wr_doc(ntcfg.doc)
        else:
            print(ntcfg.error)

    def wr_doc(self, doc):
        """Write a global cfg file"""
        TOMLFile(self.filename).write(doc)
        debug('  WROTE: %s', self.filename)

    def wr_ini_project(self, project, fcfgproj, quiet=False):
        """Add a project if needed & write; return if not"""
        if not exists(self.filename):
            self._chk_global_dir()
            if not quiet:
                print(f'Initialized global timetracker config: {self.filename}')
            return self._wr_project_init(project, fcfgproj)
        # ntcfg: doc error
        ntcfg = read_config(self.filename)
        doc = ntcfg.doc
        if doc is not None and self._add_project(doc, project, fcfgproj):
            self.wr_doc(doc)
            if not quiet:
                print(f'Added project to the global timetracker config: {self.filename}:')
                print(f'  project: {project}; config: {fcfgproj}')
        return ntcfg

    def reinit(self, project, fcfgproj):
        """Read the global config file & only change `project` & `csv.filename`"""
        debug('CfgGlobal(%s).reinit: project=%s fcfgproj=%s', self.filename, project, fcfgproj)
        ntcfg = read_config(self.filename)
        doc = ntcfg.doc
        if doc and 'projects' in doc:
            if self._add_project(doc, project, fcfgproj):
                self.wr_doc(doc)
            else:
                print(f'No changes needed to project({project}) config: {self.filename}')
            return
        self._err_reinit(ntcfg)

    def _err_reinit(self, ntcfg):
        if ntcfg.doc is None:
            print(f'NO `projects` found in global config file: {self.filename}')
            raise ntcfg.error
        raise KeyError(f'NO `projects` found in global config file: {self.filename}')

    # -------------------------------------------------------------
    def _chk_global_dir(self):
        dir_global = op.dirname(self.filename)
        if exists(dir_global) and op.isdir(dir_global) or dir_global == '':
            return
        raise NotADirectoryError(f'{dir_global}\n'
            f'Directory for global config does not exist({dir_global})\n'
            f'Cannot create global config filename: {self.filename}'
        )

    def _add_project(self, doc, project, fcfgproj):
        """Add a project to the global config file, if it is not already present"""
        debug('CfgGlobal _add_project(%s, %s)', project, fcfgproj)
        assert op.isabs(fcfgproj), f'CfgGlobal._add_project(...) cfg NOT abs path: {fcfgproj}'
        debug('CfgGlobal %s', doc)
        # If project is not already in global config
        if self._noproj(doc, project, fcfgproj):
            debug('CfgGlobal add_line %15s %s', project, fcfgproj)
            doc['projects'].add_line((project, fcfgproj))
            return fcfgproj
        return None

    def _noproj(self, doc, projnew, projcfgname):
        """Test if the project is missing from the global config file"""
        for projname, cfgname in doc['projects']:
            debug('CfgGlobal %15s %s', projname, cfgname)
            if projname == projnew:
                if cfgname == projcfgname:
                    # Project is already in the global config file
                    return False
                debug('OLD cfgname: %s', cfgname)
                debug('NEW cfgname: %s', projcfgname)
                return True
        # Project is not in global config file
        return True

    def _wr_project_init(self, project, fcfgproj):
        doc = self._get_new_doc()
        ##print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD", doc)
        ##print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD", project)
        ##print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD", fcfgproj)
        doc['projects'].add_line((project, fcfgproj))
        ##TOMLFile(self.filename).write(doc)
        err = write_config(self.filename, doc)
        if err:
            print(f'WRITE ERROR {err}')
        return self.NTWRCFG(doc=doc, error=err)

    def _get_docprt(self, doc):
        doc_cur = doc.copy()
        ##truehome = expanduser('~')
        dirhome = op.dirname(self.filename)
        for idx, (projname, projdir) in enumerate(doc['projects'].unwrap()):
            ##pdir = op.relpath(op.abspath(projdir), truehome)
            ##pdir = op.relpath(op.abspath(projdir), dirhome)
            ##if pdir[:2] != '..':
            if has_homedir(dirhome, op.abspath(projdir)):
                ##pdir = op.join('~', pdir)
                pdir = op.join('~', op.relpath(op.abspath(projdir), dirhome))
                doc_cur['projects'][idx] = [projname, pdir]
                debug('CFGGLOBAL XXXXXXXXXXX %20s %s', projname, pdir)
        return doc_cur

    def _get_new_doc(self):
        doc = tomlkit.document()
        doc.add(tomlkit.comment("TimeTracker global configuration file"))
        doc.add(tomlkit.nl())
        arr = tomlkit.array()
        arr.multiline(True)
        doc["projects"] = arr
        return doc


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
