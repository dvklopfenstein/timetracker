"""List the location of the csv file(s)"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import dirname
from os.path import exists
from timetracker.cfg.cfg import Cfg
from timetracker.cmd.common import str_uninitialized


def cli_run_projects(fnamecfg, args):
    """Stop the timer and record this time unit"""
    cfg = Cfg(fnamecfg)
    cfg.set_cfg_global()
    run_projects(cfg, args.exists, args.rm_missing)


def run_projects(cfg, show_exists=False, rm_missing=False):
    """Show the projects listed in the global config"""
    cfg_glb = cfg.cfg_glb
    if not str_uninitialized(cfg_glb.filename):
        if not rm_missing:
            _show_projects(cfg_glb, show_exists)
        else:
            _rm_missing_projects(cfg_glb)

def _show_projects(cfg_glb, show_exists=False):
    """Show the projects listed in the global config"""
    proj_cfgs = cfg_glb.get_projects()
    if proj_cfgs:
        print(f'{len(proj_cfgs)} projects listed in global config: {cfg_glb.filename}')
        if not show_exists:
            for proj, pcfg in proj_cfgs:
                print(f'    {proj:25} {dirname(pcfg)}')
        else:
            for proj, pcfg in proj_cfgs:
                print(f'exists({int(exists(pcfg))})    {proj:25} {dirname(pcfg)}')
    else:
        print(f'There are no projects in {cfg_glb.filename}')

def _rm_missing_projects(cfg_glb):
    """Remove projects from the global config if the .timetracker dir does not exist"""
    proj_cfgs = cfg_glb.get_projects()
    projs_exist = [(p, c) for p, c in proj_cfgs if exists(c)]
    num_orig = len(proj_cfgs)
    num_exist = len(projs_exist)
    if num_exist < num_orig:
        cfg_glb.set_projects(projs_exist)
        print(f'Kept {num_exist} existing projects of '
              f'the {num_orig} listed projects '
              f'in {cfg_glb.filename}')
    else:
        print(f'All {num_orig} projects exist; none removed from list')



# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
