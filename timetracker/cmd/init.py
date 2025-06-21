"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from timetracker.cfg.cfg import Cfg


def cli_run_init(fnamecfg, args):
    """initialize timetracking on a project"""
    cfg = Cfg(fnamecfg)
    if not args.force:
        return run_init(
            cfg,
            args.dirgit,
            args.csvdir,
            project=args.project,
            trk_dir=args.trk_dir,
            fcfg_global=args.global_config_file,
            no_git_add=args.no_git_add)
    return cfg.reinit(
        args.dirgit,
        args.project,
        args.csvdir,
        fcfg_global=args.global_config_file)

def run_init(cfg, dirgit, dircsv=None, project=None, **kwargs):
    """Initialize timetracking on a project"""
    # Initialize the local configuration file for a timetracking project
    cfg_loc = cfg.cfg_loc
    fcfg_global = kwargs.get('fcfg_global')
    ##res = _chk_global_cfg(cfg_loc, project, fcfg_global)
    dirhome = kwargs.get('dirhome')
    quiet = kwargs.get('quiet')
    if (msg := cfg.needs_reinit(dircsv, project, fcfg_global, dirhome)):
        if not quiet:
            print(msg)
            sys_exit(0)
    # WRITE A LOCAL PROJECT CONFIG FILE: ./.timetracker/config
    if not cfg_loc.file_exists():
        cfg.init(dirgit, project, dircsv, fcfg_global, dirhome, quiet=quiet,
                 no_git_add=kwargs.get('no_git_add', False))
    elif not quiet:
        # pylint: disable=import-outside-toplevel
        from timetracker.msgs import str_tostart
        print(str_tostart())
    return cfg


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
