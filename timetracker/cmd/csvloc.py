"""Show information regarding the location of the csv files"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
from os.path import dirname
from logging import debug
#from timetracker.cfg.cfg_global import CfgGlobal
from timetracker.utils import yellow
from timetracker.cfg.utils import get_dirhome_globalcfg
from timetracker.cfg.utils import run_cmd
from timetracker.cfg.cfg_local import CfgProj


def cli_run_csvloc(fnamecfg, args):
    """Show information regarding the location of the csv files"""
    run_csvlocate(
        fnamecfg,
        args.csvdir,
        args.project,
        args.quiet)

def run_csvlocate(fnamecfg, dircsv, project, quiet=True):
    """Initialize timetracking on a project"""
    cfgproj = run_csvlocate_local(fnamecfg, dircsv, project, quiet)
    debug(cfgproj.get_desc("new"))
    dirhome = get_dirhome_globalcfg()
    assert dirhome

def run_csvlocate_test(fnamecfg, dircsv, project, dirhome):
    """Initialize timetracking on a test project"""
    cfgproj = run_csvlocate_local(fnamecfg, dircsv, project, False)
    debug(run_cmd(f'cat {fnamecfg}'))
    assert dirhome
    return cfgproj

def run_csvlocate_local(fnamecfg, dircsv, project, quiet=True):
    """Initialize the local configuration file for a timetracking project"""
    debug(yellow('RUNNING COMMAND CSVLOC'))
    debug(f'CSVLOC: fnamecfg:    {fnamecfg}')
    debug(f'CSVLOC: project:     {project}')
    debug(f'CSVLOC: dircsv:      {dircsv}')
    if exists(fnamecfg):
        print(f'Trk repository already initialized: {dirname(fnamecfg)}')
        sys_exit(0)
    cfgproj = CfgProj(fnamecfg, project)
    # WRITE A LOCAL PROJECT CONFIG FILE: ./.timetracker/config
    cfgproj.write_file(quiet=quiet)
    return cfgproj


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
