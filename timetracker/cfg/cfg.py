"""Configuration manager for timetracker"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from os.path import relpath
from logging import debug
from timetracker.cfg.cfg_global import get_cfgglobal
from timetracker.cfg.cfg_global import CfgGlobal
from timetracker.cfg.cfg_local  import CfgProj
from timetracker.cfg.doc_local import get_docproj
from timetracker.cfg.doc_local import get_ntdocproj
from timetracker.cfg.docutils import get_value
from timetracker.cfg.utils import get_filename_globalcfg
from timetracker.proc import git_add


class Cfg:
    """Configuration manager for timetracker"""

    def __init__(self, fcfg_local, cfg_global=None):
        # TBD: param cfgproj
        self.cfg_loc = CfgProj(fcfg_local)
        self.cfg_glb = cfg_global
        # pylint: disable=line-too-long
        debug('Cfg exists(%d) Cfg(%s)', int(exists(self.cfg_loc.filename)), self.cfg_loc.filename)

    def get_projects(self, dirhome=None, fcfg_global=None):
        """Get a list of projects from the global config file"""
        if self.cfg_glb is None:
            self.set_cfg_global(fcfg_global, dirhome)
        return self.cfg_glb.get_projects()

    def set_cfg_global(self, fcfg_global=None, dirhome=None):
        """Create and set `cfg_glb` with a CfgGlobal object"""
        fcfg_doc = get_value(get_docproj(self.cfg_loc.filename), 'global_config', 'filename')
        self.cfg_glb = get_cfgglobal(fcfg_global, dirhome, fcfg_doc)

    def needs_reinit(self, dircsv, project, fcfg_global, dirhome=None):
        """Check to see if CfgProj needs to be re-initialized"""
        debug('Cfg.needs_reinit(dircsv=%s, project=%s, fcfg_global=%s, dirhome=%s)',
              dircsv, project, fcfg_global, dirhome)
        if dircsv is None and project is None and fcfg_global is None:
            return None
        docproj = get_docproj(self.cfg_loc.filename)
        if docproj is None:
            return None
        msg = []
        if project is not None and (proj_orig := docproj.project) != project:
            msg.append(f'  * change project from "{proj_orig}" to "{project}"')
        # pylint: disable=line-too-long
        ##if fcfg_global is not None and (fcfgg_orig := docproj.global_config_filename) != fcfg_global:
        if fcfg_global is not None and \
            (fcfgg_orig := get_filename_globalcfg(fcfg_doc=docproj.global_config_filename)) != fcfg_global:
            msg.append(f'  * change the global config filename\n'
                       f'        from: "{fcfgg_orig}"\n'
                       f'        to:   "{fcfg_global}"')
        # pylint: disable=fixme
        # TODO: Ensure dircsv is normpathed, abspathed
        if self._needs_reinit_fcsv(docproj, dircsv):
            msg.append(f'  * change the csv directory from "{docproj.dircsv}" to "{dircsv}"')
        if msg:
            msg = ['Use `--force` with the `init` command to:'] + msg
            return '\n'.join(msg)
        # TODO: Check global config
        return None

    def init(self, dirgit, project=None, dircsv=None, fcfg_global=None, dirhome=None, **kwargs):
        """Initialize a project, return CfgGlobal"""
        # pylint: disable=unknown-option-value,too-many-arguments,too-many-positional-arguments
        ##print(f'Cfg.init(\n  {dirgit=},\n  {project=},\n  {dircsv=},\n'  # DVK
        ##      f'  {fcfg_global=},\n  {dirhome=},\n  {kwargs})')
        project = self._get_project(project)
        quiet = kwargs.get('quiet')
        self._init_localproj(dirgit, project, dircsv, fcfg_global, quiet,
                             kwargs.get('no_git_add', False))
        if self.cfg_glb is None:
            self.set_cfg_global(fcfg_global, dirhome)
        debug('INIT CfgGlobal filename %s', self.cfg_glb.filename)
        return self.cfg_glb.wr_ini_project(project, self.cfg_loc.filename, quiet=quiet)

    def _init_localproj(self, dirgit, project, dircsv, fcfg_global, quiet, no_git_add):
        """Initialize local project"""
        # pylint: disable=unknown-option-value,too-many-arguments,too-many-positional-arguments
        ntcfg = self.cfg_loc.wr_ini_file(project, dircsv, fcfg_global)
        ntgit = self.cfg_loc.wr_gitignore()
        if dirgit is not None and not no_git_add:
            files = self._git_add(ntcfg, ntgit)
            if files:
                filestr = ' '.join(relpath(f) for f in files)
                print(f'Ran `git add {filestr}`')
        if not quiet:
            print(f'Initialized project directory: {self.cfg_loc.dircfg}')

    def reinit(self, dirgit, project=None, dircsv=None, fcfg_global=None, dirhome=None):
        """Re-initialize the project, keeping existing files"""
        # pylint: disable=unknown-option-value,too-many-arguments,too-many-positional-arguments
        ##print(f'Cfg.reinit(\n  {dirgit=},\n  {project=},\n  '  # DVK
        ##      f'{dircsv=},\n  {fcfg_global=},\n  {dirhome=})')
        assert self.cfg_loc is not None

        # pylint: disable=line-too-long
        self._reinit_loc_main(dirgit, project, dircsv, fcfg_global, dirhome)
        self._reinit_glb_main(fcfg_global, dirhome, self.cfg_loc.filename)

    def _get_project(self, project):
        if project is None:
            project = self.cfg_loc.get_project_from_filename()
        assert project is not None
        return project

    def _git_add(self, ntcfg, ntgit):
        files = []
        if ntcfg.error is None:
            files.append(ntcfg.filename)
        if ntgit.error is None:
            files.append(ntgit.filename)
        if files:
            ntrsp = git_add(files)
            if ntrsp is not None and ntrsp.returncode == 0:
                return files
        return None

    # pylint: disable=unknown-option-value,too-many-arguments,too-many-positional-arguments
    def _reinit_loc_main(self, dirgit, project, dircsv, fcfg_global, dirhome):
        ntdoc = get_ntdocproj(self.cfg_loc.filename)
        if ntdoc.doc is None:
            self.init(dirgit, project, dircsv, fcfg_global, dirhome)
            return
        if project is None:
            project = ntdoc.docproj.project
        assert project is not None
        if not exists(self.cfg_loc.filename):
            self.cfg_loc.wr_ini_file(project, dircsv, fcfg_global)
            print(f'Initialized timetracker directory: {self.cfg_loc.dircfg}')
        else:
            self.cfg_loc.reinit(project, dircsv, fcfg_global, ntdoc)

    def _reinit_glb_main(self, fcfg_global, dirhome, fcfg_loc):
        docproj = get_docproj(fcfg_loc)
        # pylint: disable=line-too-long
        fcfg_glb = get_filename_globalcfg(dirhome, fcfg_global, docproj.global_config_filename)
        assert fcfg_glb is not None
        if self.cfg_glb:
            debug('_reinit_global %s', self.cfg_glb.filename)
        debug('_reinit_global fcfg_global=%s', fcfg_global)
        debug('_reinit_global fcfg_glb=%s', fcfg_glb)
        assert docproj is not None
        assert docproj.project is not None
        debug('_reinit_glb_exp0(\n  docproj.project=%s,\n  fcfg_global=%s,\n  dirhome=%s,\n  fcfg_loc=%s)',
            docproj.project, fcfg_global, dirhome, fcfg_loc)
        if self.cfg_glb is None:
            self.cfg_glb = CfgGlobal(fcfg_glb)
        elif self.cfg_glb.filename != fcfg_glb:
            self.cfg_glb.filename = fcfg_glb

        if not exists(self.cfg_glb.filename):
            self.cfg_glb.wr_ini_project(docproj.project, fcfg_loc)
        else:
            self.cfg_glb.reinit(docproj.project, fcfg_loc)

    @staticmethod
    def _needs_reinit_fcsv(docproj, dircsv):
        if dircsv is None:
            return False
        if docproj.dircsv == dircsv:
            return False
        if docproj.get_abspath_dircsv() == dircsv:
            return False
        return True


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
