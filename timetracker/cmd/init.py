"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
from os.path import dirname
from logging import debug
from timetracker.cfg.cfg_global import CfgGlobal
from timetracker.cfg.cfg_global import get_dirhome_globalcfg
from timetracker.cfg.cfg_local  import CfgProj
from timetracker.cfg.utils  import run_cmd



def cli_run_init(fnamecfg, args):
    """initialize timetracking on a project"""
    run_init(
        fnamecfg,
        args.csvdir,
        args.project,
        args.quiet)

def run_init(fnamecfg, dircsv, project, quiet=True):
    """Initialize timetracking on a project"""
    cfgproj = run_init_local(fnamecfg, dircsv, project, quiet)
    dirhome = get_dirhome_globalcfg()
    run_init_global(dirhome, cfgproj)

def run_init_test(fnamecfg, dircsv, project, dirhome):
    """Initialize timetracking on a test project"""
    cfgproj = run_init_local(fnamecfg, dircsv, project, False)
    debug(run_cmd(f'cat {fnamecfg}'))
    cfg_global = run_init_global(dirhome, cfgproj)
    return cfgproj, cfg_global

def run_init_local(fnamecfg, dircsv, project, quiet=True):
    """Initialize the local configuration file for a timetracking project"""
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
    return cfgproj

def run_init_global(dirhome, cfgproj):
    """Initialize the global configuration file for a timetracking project"""
    # 4. WRITE A GLOBAL TIMETRACKER CONFIG FILE: ~/.timetrackerconfig, if needed
    cfg_global = CfgGlobal(dirhome)
    chgd = cfg_global.add_proj(cfgproj.project, cfgproj.get_filename_cfg())
    if chgd:
        cfg_global.wr_cfg()
    return cfg_global


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
