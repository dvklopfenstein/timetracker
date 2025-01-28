"""Global configuration parser for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import environ
##from os import getcwd
from os.path import exists
##from os.path import basename
from os.path import expanduser
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
##from timetracker.cfg.utils import replace_envvar
##from timetracker.cfg.utils import get_dirname_abs
##from timetracker.cfg.utils import chk_isdir
##from timetracker.cfg.utils import replace_homepath
from timetracker.cfg.utils import parse_cfg


class CfgGlobal:
    """Global configuration parser for timetracking"""

    def __init__(self, cfgdir='~', basename='.timetrackerconfig'):
        self.cfgdir = normpath(abspath(self._init_cfgdir(cfgdir)))
        self.fname = join(self.cfgdir, basename)
        debug(f'CFG GLOBAL CONFIG: exists({int(exists(self.fname))}) -- {self.fname}')
        self.docini = self._init_docglobal()

    def str_cfg(self):
        """Return string containing configuration file contents"""
        return dumps(self.docini)

    def rd_cfg(self):
        """Read a global cfg file; return a doc obj"""
        return parse_cfg(self.fname)

    def wr_cfg(self):
        """Write config file"""
        projects = self.docini['projects']
        debug(f'CFG WRITING GLOBAL PROJECTS: {projects}')
        with open(self.fname, 'w', encoding='utf8') as ostrm:
            print(self.str_cfg(), file=ostrm, end='')
            debug(f'  WROTE: {self.fname}')

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
        doc["projects"] = []
        return doc

    def _init_cfgdir(self, cfgdir):
        if cfgdir == '~':
            return expanduser(cfgdir)
        if exists(cfgdir):
            return cfgdir
        if hasattr(environ, cfgdir):
            ret = environ[cfgdir]
            if exists(ret):
                return ret
            raise RuntimeError(f'NO DIRECTORY IN ENVVAR {cfgdir}: {cfgdir}')
        raise RuntimeError(f'UNKNOWN DIRECTORY FOR GLOBAL CONFIGURATION: {cfgdir}')

    #def _init_fname(self):
    #    pass


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
