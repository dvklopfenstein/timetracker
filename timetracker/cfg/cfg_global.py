"""Global configuration parser for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

##from os import getcwd
from os.path import exists
##from os.path import basename
from os.path import join
from os.path import abspath
##from os.path import relpath
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
from timetracker.cfg.utils import get_cfgdir


class CfgGlobal:
    """Global configuration parser for timetracking"""

    def __init__(self, cfgdir='~', basename='.timetrackerconfig'):
        self.cfgdir = normpath(abspath(get_cfgdir(cfgdir)))
        self.fname = join(self.cfgdir, basename)
        debug(f'CFG GLOBAL CONFIG: exists({int(exists(self.fname))}) -- {self.fname}')
        self.doc = self._init_docglobal()

    def str_cfg(self):
        """Return string containing configuration file contents"""
        return dumps(self.doc)

    def rd_cfg(self):
        """Read a global cfg file; return a doc obj"""
        return TOMLFile(self.fname).read()

    def wr_cfg(self):
        """Write config file"""
        projects = self.doc['projects']
        debug(f'CFG WRITING GLOBAL PROJECTS: {projects}')
        TOMLFile(self.fname).write(self.doc)
        debug(f'  WROTE: {self.fname}; PROJECTS: ')

    def add_proj(self, project, cfgfilename):
        """Add a project to the global config file, if it is not already present"""
        doc = self.rd_cfg()
        if self._noproj(doc, project, cfgfilename):
            doc['projects'].add_line((project, cfgfilename))
            self.doc = doc


    def _noproj(self, doc, projnew, projcfgname):
        """Test if the project is missing from the global config file"""
        for projname, cfgname in doc['projects']:
            if projname == projnew:
                if cfgname == projcfgname:
                    return False
                raise RuntimeError('PROJECT({projname}) {projcfgname} != {cfgname}')
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

    #def _init_fname(self):
    #    pass


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
