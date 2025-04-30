"""Global configuration parser for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

##from os import getcwd
##from os import environ
from os.path import isabs
from os.path import isdir
from os.path import exists
from os.path import dirname
##from os.path import expanduser
##from os.path import basename
from os.path import join
from os.path import abspath
from os.path import relpath
from logging import debug
from collections import namedtuple

from tomlkit import comment
from tomlkit import document
from tomlkit import nl
from tomlkit import array
from tomlkit.toml_file import TOMLFile

##from timetracker.cfg.utils import replace_homepath
####from timetracker.consts import FILENAME_GLOBALCFG
from timetracker.utils import ltblue
##from timetracker.cfg.utils import get_dirhome
from timetracker.cfg.tomutils import read_config
from timetracker.cfg.tomutils import write_config
from timetracker.cfg.utils import has_homedir
from timetracker.cfg.utils import get_filename_globalcfg
#from timetracker.cfg.utils import get_relpath_adj
#from timetracker.consts import FILENAME_GLOBALCFG


def get_cfgglobal(fcfg_explicit=None, dirhome=None, fcfg_doc=None):
    """Get a global configuration object"""
    return CfgGlobal(get_filename_globalcfg(dirhome, fcfg_explicit, fcfg_doc))


class CfgGlobal:
    """Global configuration parser for timetracking"""

    NTWRCFG = namedtuple('WrCfg', 'doc error')

    def __init__(self, filename):
        self.filename = filename
        debug(ltblue(f'CfgGlobal CONFIG: exists({int(exists(filename))}) -- {filename}'))

    def get_projects(self):
        """Get the projects managed by timetracker"""
        ntcfg = read_config(self.filename)
        if ntcfg.doc:
            return ntcfg.doc.get('projects')
        return None

    def wr_doc(self, doc):
        """Write a global cfg file"""
        TOMLFile(self.filename).write(doc)
        debug(ltblue(f'  SSS WROTE: {self.filename}'))

    def wr_ini_project(self, project, fcfgproj):
        """Add a project if needed & write; return if not"""
        if not exists(self.filename):
            self._chk_global_dir()
            print(f'Initialized global timetracker config: {self.filename}')
            return self._wr_project_init(project, fcfgproj)
        # ntcfg: doc error
        ntcfg = read_config(self.filename)
        doc = ntcfg.doc
        if doc is not None and self._add_project(doc, project, fcfgproj):
            self.wr_doc(doc)
            print(f'Added project to the global timetracker config: {self.filename}:')
            print(f'  project: {project}; config: {fcfgproj}')
        return ntcfg

    def reinit(self, project, fcfgproj):
        """Read the global config file & only change `project` & `csv.filename`"""
        debug(ltblue(f'CfgGlobal({self.filename}).reinit: {project=} {fcfgproj=}'))
        ntcfg = read_config(self.filename)
        doc = ntcfg.doc
        if doc:
            if self._add_project(doc, project, fcfgproj):
                self.wr_doc(doc)
            else:
                print(f'No changes needed to project({project}) config: {self.filename}')

    # -------------------------------------------------------------
    def _chk_global_dir(self):
        dir_global = dirname(self.filename)
        if exists(dir_global) and isdir(dir_global) or dir_global == '':
            return
        raise NotADirectoryError(f'{dir_global}\n'
            f'Directory for global config does not exist({dir_global})\n'
            f'Cannot create global config filename: {self.filename}'
        )

    def _add_project(self, doc, project, fcfgproj):
        """Add a project to the global config file, if it is not already present"""
        debug(ltblue(f'CfgGlobal _add_project({project}, {fcfgproj}'))
        assert isabs(fcfgproj), f'CfgGlobal._add_project(...) cfg NOT abspath: {fcfgproj}'
        debug(ltblue(f'CfgGlobal {doc}'))
        # If project is not already in global config
        if self._noproj(doc, project, fcfgproj):
            debug(f'CfgGlobal add_line {project:15} {fcfgproj}')
            doc['projects'].add_line((project, fcfgproj))
            return fcfgproj
        # pylint: disable=unsubscriptable-object
        ##debug(f"PROJECT {project} IN GLOBAL PROJECTS: {doc['projects'].as_string()}")
        return None

    def _noproj(self, doc, projnew, projcfgname):
        """Test if the project is missing from the global config file"""
        for projname, cfgname in doc['projects']:
            debug(f'CfgGlobal {projname:15} {cfgname}')
            if projname == projnew:
                if cfgname == projcfgname:
                    # Project is already in the global config file
                    return False
                debug(f'OLD cfgname: {cfgname}')
                debug(f'NEW cfgname: {projcfgname}')
                return True
        # Project is not in global config file
        return True

    def _wr_project_init(self, project, fcfgproj):
        doc = self._get_new_doc()
        doc['projects'].add_line((project, fcfgproj))
        ##TOMLFile(self.filename).write(doc)
        err = write_config(self.filename, doc)
        if err:
            print(f'WRITE ERROR {err}')
        debug(ltblue(f'CfgGlobal WRINI({self.filename}): {doc["projects"]}'))
        return self.NTWRCFG(doc=doc, error=err)

    def _get_docprt(self, doc):
        doc_cur = doc.copy()
        ##truehome = expanduser('~')
        dirhome = dirname(self.filename)
        for idx, (projname, projdir) in enumerate(doc['projects'].unwrap()):
            ##pdir = relpath(abspath(projdir), truehome)
            ##pdir = relpath(abspath(projdir), dirhome)
            ##if pdir[:2] != '..':
            if has_homedir(dirhome, abspath(projdir)):
                ##pdir = join('~', pdir)
                pdir = join('~', relpath(abspath(projdir), dirhome))
                doc_cur['projects'][idx] = [projname, pdir]
                debug(f'CFGGLOBAL XXXXXXXXXXX {projname:20} {pdir}')
        return doc_cur

    @staticmethod
    def _get_new_doc():
        doc = document()
        doc.add(comment("TimeTracker global configuration file"))
        doc.add(nl())
        arr = array()
        arr.multiline(True)
        doc["projects"] = arr
        return doc

    ##def _init_doc(self):
    ##    return TOMLFile(self.filename).read() if exists(self.filename) else self._get_new_doc()

    ##def _noproj(self, doc, projnew, projcfgname):
    ##    """Test if the project is missing from the global config file"""
    ##    for projname, cfgname in doc['projects']:
    ##        debug(f'CfgGlobal {projname:15} {cfgname}')
    ##        if projname == projnew:
    ##            if cfgname == projcfgname:
    ##                # Project is already in the global config file
    ##                return False
    ##            debug(f'OLD cfgname: {cfgname}')
    ##            debug(f'NEW cfgname: {projcfgname}')
    ##            ##raise RuntimeError(f'ERROR: Project({projname}) config filename '
    ##            ##                    'is already set to:\n'
    ##            ##                   f'        {cfgname}\n'
    ##            ##                    '    Not over-writing with:\n'
    ##            ##                   f'        {projcfgname}\n'
    ##            ##                   f'    In {self.filename}\n'
    ##            ##                    '    Use arg, `--project` to create a unique project name')
    ##            return True
    ##    # Project is not in global config file
    ##    return True

    ##def wr_cfg(self):
    ##    """Write config file"""
    ##    docprt = self._get_docprt()
    ##    TOMLFile(self.filename).write(docprt)
    ##    debug(f'CFGGLOBAL  WROTE: {self.filename}')

    ##def wr_new(self):
    ##    """Write config file"""
    ##    docini = self._init_doc()
    ##    docprt = self._get_docprt(docini)

    #@staticmethod
    #def _init_dirhome(filename):
    #    if isdir(filename):
    #        return filename, FILENAME_GLOBALCFG
    #    if filename.endswith(FILENAME_GLOBALCFG):
    #        return dirname, filename

    ##    TOMLFile(self.filename).write(docprt)
    ##    debug(f'CFGGLOBAL  WROTE: {self.filename}')

    ##def _add_project(self, project, cfgfilename):
    ##    """Add a project to the global config file, if it is not already present"""
    ##    assert isabs(cfgfilename), f'CfgGlobal._add_project(...) cfg NOT abspath: {cfgfilename}'
    ##    doc = self.rd_cfg()
    ##    # If project is not already in global config
    ##    if self._noproj(doc, project, cfgfilename):
    ##        fnamecfg_proj = cfgfilename
    ##        ##if has_homedir(self.dirhome, abspath(cfgfilename)):
    ##        ##    ##cfgfilename = join('~', relpath(abspath(cfgfilename), self.dirhome))
    ##        ##    ##fnamecfg_proj = get_relpath_adj(abspath(cfgfilename), self.dirhome)
    ##        ##    ##debug(f'OOOOOOOOOO {fnamecfg_proj}')
    ##        if doc is not None:
    ##            doc['projects'].add_line((project, fnamecfg_proj))
    ##            self.doc = doc
    ##        else:
    ##            self.doc['projects'].add_line((project, fnamecfg_proj))
    ##        ##debug(f"PROJECT {project} ADD GLOBAL PROJECTS: {self.doc['projects'].as_string()}")
    ##        return True
    ##    # pylint: disable=unsubscriptable-object
    ##    ##debug(f"PROJECT {project} IN GLOBAL PROJECTS: {doc['projects'].as_string()}")
    ##    return False

    ##def _add_project(self, doc, project, cfgfilename):
    ##    """Add a project to the global config file, if it is not already present"""
    ##    debug(ltblue(f'CfgGlobal _add_project({project}, {cfgfilename}'))
    ##    assert isabs(cfgfilename), f'CfgGlobal._add_project(...) cfg NOT abspath: {cfgfilename}'
    ##    ####if not exists(self.filename):
    ##    ####    return self._wr_project_init(project, cfgfilename)
    ##    #### doc = TOMLFile(self.filename).read()
    ##    debug(ltblue(f'CfgGlobal {doc}'))
    ##    # If project is not already in global config
    ##    if self._noproj(doc, project, cfgfilename):
    ##        debug(f'CfgGlobal add_line {project:15} {cfgfilename}')
    ##        ##if has_homedir(self.dirhome, abspath(cfgfilename)):
    ##        ##    ##cfgfilename = join('~', relpath(abspath(cfgfilename), self.dirhome))
    ##        ##    ##fnamecfg_proj = get_relpath_adj(abspath(cfgfilename), self.dirhome)
    ##        ##    ##debug(f'OOOOOOOOOO {fnamecfg_proj}')
    ##        doc['projects'].add_line((project, cfgfilename))
    ##        ##debug(f"PROJECT {project} ADD GLOBAL PROJECTS: {doc['projects'].as_string()}")
    ##        return True
    ##    # pylint: disable=unsubscriptable-object
    ##    ##debug(f"PROJECT {project} IN GLOBAL PROJECTS: {doc['projects'].as_string()}")
    ##    return False

# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
