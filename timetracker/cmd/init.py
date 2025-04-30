"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
from logging import debug
from timetracker.utils import yellow
from timetracker.cfg.cfg import Cfg
from timetracker.msgs import str_tostart


def cli_run_init(fnamecfg, args):
    """initialize timetracking on a project"""
    if not args.force:
        run_init(
            fnamecfg,
            args.csvdir,
            project=args.project,
            trk_dir=args.trk_dir,
            fcfg_global=args.global_config_file)
    else:
        run_reinit(
            fnamecfg,
            args.csvdir,
            project=args.project,
            trk_dir=args.trk_dir,
            fcfg_global=args.global_config_file)

def run_init(fnamecfg, dircsv=None, project=None, **kwargs):
    """Initialize timetracking on a project"""
    cfg = Cfg(fnamecfg, cfg_global=kwargs.get('cfg_global'))
    # Initialize the local configuration file for a timetracking project
    cfg_loc = cfg.cfg_loc
    debug(yellow('RUNNING COMMAND INIT'))
    debug(f'INIT: fnamecfg:    {cfg_loc.filename}')
    debug(f'INIT: project:     {project}')
    debug(f'INIT: dircsv({dircsv})')
    fcfg_global = kwargs.get('fcfg_global')
    ##res = _chk_global_cfg(cfg_loc, project, fcfg_global)
    dirhome = kwargs.get('dirhome')
    if (msg := cfg.needs_reinit(dircsv, project, fcfg_global, dirhome)):
        print(msg)
        sys_exit(0)
    # WRITE A LOCAL PROJECT CONFIG FILE: ./.timetracker/config
    if not exists(cfg_loc.filename):
        debug('CMD INIT <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        cfg.init(project, dircsv, fcfg_global, dirhome)
        debug('CMD INIT >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        debug(cfg.cfg_loc.get_desc("ran_init"))
    else:
        print(str_tostart())
    return cfg

##def _chk_global_cfg(cfg_loc, project, fcfg_global):
##    if fcfg_global is None or cfg_loc.exists:
##        return
##    print(f'Use `--force` with the `init` command to initialize global config: {fcfg_global}')

def run_reinit(fnamecfg, dircsv, project, **kwargs):
    """Reinitialize timetracking project"""
    cfg = Cfg(fnamecfg)
    cfg.reinit(project, dircsv, kwargs.get('fcfg_global'), kwargs.get('dirhome'))
    return cfg


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
