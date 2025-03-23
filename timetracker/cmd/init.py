"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
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
            fcfg_global=args.file)
    else:
        run_reinit(
            fnamecfg,
            args.csvdir,
            project=args.project,
            fcfg_global=args.file)

def run_init(fnamecfg, dircsv, project, **kwargs):
    """Initialize timetracking on a project"""
    cfg = Cfg(fnamecfg, kwargs.get('fcfg_global'), kwargs.get('dirhome'))
    # Initialize the local configuration file for a timetracking project
    cfg_loc = cfg.cfg_loc
    debug(yellow('RUNNING COMMAND INIT'))
    debug(f'INIT: fnamecfg:    {cfg_loc.filename}')
    debug(f'INIT: project:     {project}')
    debug(f'INIT: dircsv({dircsv})')
    if cfg_loc.exists:
        print(str_tostart())
        sys_exit(0)
    # WRITE A LOCAL PROJECT CONFIG FILE: ./.timetracker/config
    cfg_loc.write_file(project, dircsv=dircsv)
    debug(cfg.cfg_loc.get_desc("new"))
    cfg.add_project(project)
    return cfg

def run_reinit(fnamecfg, dircsv, project, **kwargs):
    """Reinitialize timetracking project"""
    cfg = Cfg(fnamecfg, kwargs.get('fcfg_global'), kwargs.get('dirhome'))
    print('FFFFFFFFFFFFFFFF', fnamecfg)
    cfg.reinit(project, dircsv=dircsv)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
