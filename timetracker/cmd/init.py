"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
from logging import debug
from timetracker.utils import yellow
from timetracker.cfg.utils import get_dirhome_globalcfg
from timetracker.cfg.cfg_global import CfgGlobal
from timetracker.cfg.cfg_local  import CfgProj
from timetracker.msgs import str_tostart



def cli_run_init(fnamecfg, args):
    """initialize timetracking on a project"""
    run_init(
        fnamecfg,
        args.csvdir,
        args.project,
        args.quiet)

def run_init(fnamecfg, dircsv, project, quiet=False):
    """Initialize timetracking on a project"""
    cfgproj = run_init_local(fnamecfg, dircsv, project, quiet)
    debug(cfgproj.get_desc("new"))
    dirhome = get_dirhome_globalcfg()
    run_init_global(dirhome, cfgproj)

def run_init_test(fnamecfg, dircsv, project, dirhome, quiet=False):
    """Initialize timetracking on a test project"""
    cfgproj = run_init_local(fnamecfg, dircsv, project, quiet)
    cfg_global = run_init_global(dirhome, cfgproj)
    return cfgproj, cfg_global

def run_init_local(fnamecfg, dircsv, project, quiet=True):
    """Initialize the local configuration file for a timetracking project"""
    debug(yellow('RUNNING COMMAND INIT'))
    debug(f'INIT: fnamecfg:    {fnamecfg}')
    debug(f'INIT: project:     {project}')
    debug(f'INIT: dircsv({dircsv})')
    if exists(fnamecfg):
        print(str_tostart())
        sys_exit(0)
    cfgproj = CfgProj(fnamecfg, project)
    # WRITE A LOCAL PROJECT CONFIG FILE: ./.timetracker/config
    cfgproj.write_file(dircsv=dircsv, quiet=quiet)
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
