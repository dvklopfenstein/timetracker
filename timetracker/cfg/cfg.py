"""Configuration manager for timetracker"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from logging import debug
from timetracker.cfg.cfg_global import get_cfgglobal
from timetracker.cfg.cfg_local  import CfgProj
from timetracker.cfg.doc_local import get_docproj
from timetracker.cfg.doc_local import get_ntdocproj
from timetracker.utils import yellow
#from timetracker.msgs import str_tostart
#from timetracker.msgs import str_init
#from timetracker.msgs import str_reinit
#from timetracker.cmd.utils import run_strinit


class Cfg:
    """Configuration manager for timetracker"""

    def __init__(self, fcfg_local, cfg_global=None):
        self.cfg_loc = CfgProj(fcfg_local)
        self.cfg_glb = cfg_global
        debug(f'Cfg exists({int(exists(self.cfg_loc.filename))}) Cfg({self.cfg_loc.filename})')
        #debug(f'Cfg exists({int(exists(self.cfg_glb.filename))}) Cfg({self.cfg_glb.filename})')

    ##def needs_init(self, fcfg_global=None, dirhome=None):
    ##    """Check for existance of both local and global config to see if init is needed"""
    ##    fgcfg = get_cfgglobal(fcfg_global, dirhome, 'need').filename
    ##    return not exists(self.cfg_loc.filename) or not exists(fgcfg)

    ##    #if (exist_loc := exists(self.cfg_loc.filename)) and (exist_glb := exists(fgcfg)):
    ##    #    return False
    ##    #if not exist_loc:
    ##    #    print(str_init(self.cfg_loc.filename))
    ##    #elif not exist_glb:
    ##    #    print(f'Global config, {fgcfg} not found')
    ##    #    print(str_reinit())
    ##    #return True

    def needs_reinit(self, dircsv, project, fcfg_global, dirhome=None):
        """Check to see if CfgProj needs to be re-initialized"""
        debug(yellow(f'Cfg.needs_reinit({dircsv=}, {project=}, {fcfg_global=}, {dirhome=})'))
        if dircsv is None and project is None and fcfg_global is None:
            return None
        docproj = get_docproj(self.cfg_loc.filename)
        if docproj is None:
            return None
        msg = []
        if project is not None and (proj_orig := docproj.project) != project:
            msg.append(f'  * change project from "{proj_orig}" to "{project}"')
        # pylint: disable=line-too-long
        if fcfg_global is not None and (fcfgg_orig := docproj.global_config_filename) != fcfg_global:
            msg.append(f'  * change the global config filename from "{fcfgg_orig}" to "{fcfg_global}"')
        # pylint: disable=fixme
        # TODO: Ensure dircsv is normpathed, abspathed
        if self._needs_reinit_fcsv(docproj, dircsv):
            msg.append(f'  * change the csv directory from "{docproj.dircsv}" to "{dircsv}"')
        if msg:
            msg = ['Use `--force` with the `init` command to:'] + msg
            return '\n'.join(msg)
        # TODO: Check global config
        return None

    def init(self, project=None, dircsv=None, fcfg_global=None, dirhome=None):
        """Initialize a project, return CfgGlobal"""
        debug(yellow(f'Cfg.init(project={project}, dirscv={dircsv}, '
                     f'fcfg_global={fcfg_global}, dirhome={dirhome})'))
        if project is None:
            project = self.cfg_loc.get_project_from_filename()
        assert project is not None
        self.cfg_loc.wr_ini_file(project, dircsv, fcfg_global)
        print(f'Initialized project directory: {self.cfg_loc.dircfg}')
        if self.cfg_glb is None:
            self.cfg_glb = get_cfgglobal(fcfg_global, dirhome)
        debug(f'INIT CfgGlobal filename {self.cfg_glb.filename}')
        return self.cfg_glb.wr_ini_project(project, self.cfg_loc.filename)

    def reinit(self, project=None, dircsv=None, fcfg_global=None, dirhome=None):
        """Re-initialize the project, keeping existing files"""
        debug(yellow(f'Cfg.reinit(project={project}, dirscv={dircsv}, '
                     f'fcfg_global={fcfg_global}, dirhome={dirhome})'))
        assert self.cfg_loc is not None
        ntdoc = get_ntdocproj(self.cfg_loc.filename)
        if ntdoc.doc is None:
            self.init(project, dircsv, fcfg_global, dirhome)
            return
        if project is None:
            project = ntdoc.docproj.project
        assert project is not None
        self._reinit_local(project, dircsv, fcfg_global, ntdoc)
        if self.cfg_glb is None:
            self.cfg_glb = get_cfgglobal(fcfg_global, dirhome)
        debug(f'REINIT CfgGlobal filename {self.cfg_glb.filename}')
        self._reinit_global(self.cfg_glb, project, self.cfg_loc.filename)
        return

    # pylint: disable=unknown-option-value,too-many-arguments,too-many-positional-arguments
    def _reinit_local(self, project, dircsv, fcfg_global, docproj):
        cfg_loc = self.cfg_loc
        if not exists(cfg_loc.filename):
            cfg_loc.wr_ini_file(project, dircsv, fcfg_global)
            print(f'Initialized timetracker directory: {cfg_loc.dircfg}')
        else:
            cfg_loc.reinit(project, dircsv, fcfg_global, docproj)

    @staticmethod
    def _reinit_global(cfg_gbl, project, fcfg_loc):
        if not exists(cfg_gbl.filename):
            cfg_gbl.wr_ini_project(project, fcfg_loc)
        else:
            cfg_gbl.reinit(project, fcfg_loc)

    @staticmethod
    def _needs_reinit_fcsv(docproj, dircsv):
        ##print(f'_needs_reinit_fcsv: docproj.dircsv               {docproj.dircsv}')
        ##print(f'_needs_reinit_fcsv: docproj.get_abspath_dircsv() {docproj.get_abspath_dircsv()}')
        ##print(f'_needs_reinit_fcsv: dircsv                       {dircsv}')
        ##print(f'_needs_reinit_fcsv: dirhome                      {dirhome}')
        if dircsv is None:
            return False
        if docproj.dircsv == dircsv:
            return False
        if docproj.get_abspath_dircsv() == dircsv:
            return False
        return True



# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
