"""Configuration manager for timetracker"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

#from sys import exit as sys_exit
from os.path import exists
from logging import debug
#from timetracker.utils import yellow
from timetracker.cfg.cfg_global import CfgGlobal
from timetracker.cfg.cfg_local  import CfgProj
from timetracker.cfg.utils import get_filename_globalcfg
#from timetracker.msgs import str_tostart
from timetracker.msgs import str_init
from timetracker.msgs import str_reinit


# pylint: disable=too-few-public-methods
class Cfg:
    """Configuration manager for timetracker"""

    ####def __init__(self, fcfg_local, fcfg_global=None, dirhome=None):
    def __init__(self, fcfg_local):
        self.cfg_loc = CfgProj(fcfg_local)
        self.cfg_glb = None
        debug(f'Cfg exists({int(exists(self.cfg_loc.filename))}) Cfg({self.cfg_loc.filename})')
        ####debug(f'{int(exists(self.cfg_glb.filename))} GLOB {self.cfg_glb.filename}')

    def needs_init(self, fcfg_global=None, dirhome=None):
        """Check for existance of both local and global config to see if init is needed"""
        fgcfg = self.get_cfgglobal(fcfg_global, dirhome).filename
        if (exist_loc := exists(self.cfg_loc.filename)) and (exist_glb := exists(fgcfg)):
            return False
        if not exist_loc:
            print(str_init(exist_loc))
        elif not exist_glb:
            print(f'Global config, {fgcfg} not found')
            print(str_reinit())
        return True

    ####def add_project(self, project):
    ####    """Add the project to the local and global config"""
    ####    return self.cfg_glb.add_project(project, self.cfg_loc.get_filename_cfg())

    def init(self, project=None, dircsv=None, fcfg_global=None, dirhome=None):
        """Initialize a project, return CfgGlobal"""
        self.cfg_loc.wr_ini_file(project, dircsv, fcfg_global)
        self.cfg_glb = self.get_cfgglobal(fcfg_global, dirhome)
        debug(f'INIT CfgGlobal filename {self.cfg_glb.filename}')
        return self.cfg_glb.wr_ini_project(project, self.cfg_loc.filename)

    def reinit(self, project, dircsv=None, fcfg_global=None, dirhome=None):
        """Re-initialize the project, keeping existing files"""
        self._reinit_local(self.cfg_loc, project, dircsv, fcfg_global)
        self.cfg_glb = self.get_cfgglobal(fcfg_global, dirhome)
        debug(f'REINIT CfgGlobal filename {self.cfg_glb.filename}')
        self._reinit_global(self.cfg_glb, project, self.cfg_loc.filename)

    @staticmethod
    def get_cfgglobal(fcfg=None, dirhome=None):
        """Get a global configuration object"""
        return CfgGlobal(get_filename_globalcfg(dirhome) if fcfg is None else fcfg)

    @staticmethod
    def _reinit_local(cfg_loc, project, dircsv, fcfg_global):
        if not exists(cfg_loc.filename):
            cfg_loc.wr_ini_file(project, dircsv, fcfg_global)
        else:
            cfg_loc.reinit(project, dircsv, fcfg_global)

    @staticmethod
    def _reinit_global(cfg_gbl, project, fcfg_loc):
        if not exists(cfg_gbl.filename):
            cfg_gbl.wr_ini_project(project, fcfg_loc)
        else:
            cfg_gbl.reinit(project, fcfg_loc)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
