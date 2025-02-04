"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
from os.path import dirname
from logging import debug
from timetracker.cfg.cfg_global import CfgGlobal
from timetracker.cfg.cfg_local  import CfgProj


def cli_run_init(fnamecfg, args):
    """initialize timetracking on a project"""
    run_init(
        fnamecfg,
        args.csvdir,
        args.project,
        args.quiet)

def run_init(fnamecfg, dircsv, project, quiet):
    """initialize timetracking on a project"""
    debug('INIT: RUNNING COMMAND INIT')
    debug(f'INIT: fnamecfg:    {fnamecfg}')
    debug(f'INIT: project:     {project}')
    debug(f'INIT: dircsv:      {dircsv}')
    if exists(fnamecfg):
        print(f'Trk repository already initialized: {dirname(fnamecfg)}')
        sys_exit()
    cfgproj = CfgProj(fnamecfg, dircsv, project)
    # 1. INITIALIZE LOCAL .timetracker PROJECT DIRECTORY
    cfgproj.mk_dircfg(quiet)
    # 2. WRITE A LOCAL PROJECT CONFIG FILE: ./.timetracker/config
    cfgproj.wr_cfg_new()
    # 3. TODO: add `start_timetracker_*.txt` to the .gitignore if this is a git-managed repo
    # 4. WRITE A GLOBAL TIMETRACKER CONFIG FILE: ~/.timetrackerconfig, if needed
    cfg_global = CfgGlobal()
    chgd = cfg_global.add_proj(cfgproj.project, cfgproj.get_filename_cfglocal())
    if chgd:
        cfg_global.wr_cfg()


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
