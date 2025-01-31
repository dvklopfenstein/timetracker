"""Global configuration parser for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

##from os import getcwd
from os.path import exists
##from os.path import expanduser
##from os.path import basename
from os.path import join
from os.path import abspath
from os.path import relpath
from os.path import normpath
from logging import debug
from tomlkit import comment
from tomlkit import document
from tomlkit import nl
##from tomlkit import table
from tomlkit import dumps
from tomlkit import array
from tomlkit.toml_file import TOMLFile
##from timetracker.cfg.utils import replace_envvar
##from timetracker.cfg.utils import get_dirname_abs
##from timetracker.cfg.utils import chk_isdir
##from timetracker.cfg.utils import replace_homepath
from timetracker.cfg.utils import parse_cfg
from timetracker.cfg.utils import get_dirhome
from timetracker.cfg.utils import has_homedir
from timetracker.cfg.utils import get_relpath_adj


class CfgGlobal:
    """Global configuration parser for timetracking"""

    def __init__(self, dirhome='~', basename='.timetrackerconfig'):
        self.dirhome = normpath(abspath(get_dirhome(dirhome)))
        self.fname = join(self.dirhome, basename)
        debug(f'CFGGLOBAL  CONFIG: exists({int(exists(self.fname))}) -- {self.fname}')
        self.doc = self._init_docglobal()

    def str_cfg(self):
        """Return string containing configuration file contents"""
        return dumps(self.doc)

    def rd_cfg(self):
        """Read a global cfg file; return a doc obj"""
        return TOMLFile(self.fname).read() if exists(self.fname) else None

    def wr_cfg(self):
        """Write config file"""
        projects = self.doc['projects'].as_string()
        docprt = self._get_docprt()
        debug(f'CFGGLOBAL WRITING GLOBAL PROJECTS: {projects}')
        TOMLFile(self.fname).write(docprt)
        debug(f'CFGGLOBAL  WROTE: {self.fname}; PROJECTS: ')

    def add_proj(self, project, cfgfilename):
        """Add a project to the global config file, if it is not already present"""
        doc = self.rd_cfg()
        # If project is not already in global config
        if self._noproj(doc, project, cfgfilename):
            fnamecfg_proj = cfgfilename
            if has_homedir(self.dirhome, cfgfilename):
                ##cfgfilename = join('~', relpath(abspath(cfgfilename), self.dirhome))
                fnamecfg_proj = get_relpath_adj(abspath(cfgfilename), self.dirhome)
                debug(f'OOOOOOOOOO {fnamecfg_proj}')
            if doc is not None:
                doc['projects'].add_line((project, fnamecfg_proj))
                self.doc = doc
            else:
                self.doc['projects'].add_line((project, fnamecfg_proj))

    def _get_docprt(self):
        doc_cur = self.doc.copy()
        ##truehome = expanduser('~')
        dirhome = self.dirhome
        for idx, (projname, projdir) in enumerate(self.doc['projects'].unwrap()):
            ##pdir = relpath(abspath(projdir), truehome)
            ##pdir = relpath(abspath(projdir), dirhome)
            ##if pdir[:2] != '..':
            if has_homedir(self.dirhome, projdir):
                ##pdir = join('~', pdir)
                pdir = join('~', relpath(abspath(projdir), dirhome))
                doc_cur['projects'][idx] = [projname, pdir]
                debug(f'CFGGLOBAL XXXXXXXXXXX {projname:20} {pdir}')
        return doc_cur

    def _noproj(self, doc, projnew, projcfgname):
        """Test if the project is missing from the global config file"""
        projs = doc['projects'] if doc is not None else self.doc['projects']
        for projname, cfgname in projs:
            if projname == projnew:
                if cfgname == projcfgname:
                    # Project is already in the global config file
                    return False
                raise RuntimeError(f'ERROR: Project({projname}) config filename '
                                    'is already set to:\n'
                                   f'        {cfgname}.\n'
                                    '    Not over-writing with:\n'
                                   f'        {projcfgname}\n'
                                   f'    In {self.fname}\n'
                                    '    Use arg, `--project` to create a unique project name')
        # Project is not in global config file
        return True

    def _init_docglobal(self):
        if not exists(self.fname):
            return self._new_docglobal()
        return parse_cfg(self.fname, 'CFG GLOBAL')

    @staticmethod
    def _new_docglobal():
        # pylint: disable=duplicate-code
        doc = document()
        doc.add(comment("TimeTracker global configuration file"))
        doc.add(nl())
        arr = array()
        arr.multiline(True)
        doc["projects"] = arr
        return doc


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
