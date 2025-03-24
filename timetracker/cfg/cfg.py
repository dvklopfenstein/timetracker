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

    def __init__(self, fcfg_local, fcfg_global=None, dirhome=None):
        self.cfg_loc = CfgProj(fcfg_local)
        # pylint: disable=line-too-long
        self.cfg_glb = CfgGlobal(get_filename_globalcfg(dirhome) if fcfg_global is None else fcfg_global)
        debug(f'{int(exists(self.cfg_loc.filename))} PROJ {self.cfg_loc.filename}')
        debug(f'{int(exists(self.cfg_glb.filename))} GLOB {self.cfg_glb.filename}')

    def needs_init(self):
        """Check for existance of both local and global config to see if init is needed"""
        if (exist_loc := exists(self.cfg_loc)) and (exist_glb := exists(self.cfg_glb)):
            return False
        if not exist_loc:
            print(str_init(self.cfg_loc.filename))
        elif not exist_glb:
            print(f'Global config, {self.cfg_glb.filename} not found')
            print(str_reinit())
        return True

    def add_project(self, project):
        """Add the project to the local and global config"""
        return self.cfg_glb.add_project(project, self.cfg_loc.get_filename_cfg())

    def reinit(self, project, dircsv):
        """Re-initialize the project, keeping existing files"""
        print('GET READY TO REINIT')
        print(f'PROJECT: {project}')
        print(f'DIRCSV:  {dircsv}')

#class CfgTrk:
#    """Manages the global and a project configuration file"""
#
#    def __init__(self, fcfg_proj, fcfg_global=None):
#        self.cfgproj = CfgProj(fcfg, project)

# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
