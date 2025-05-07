"""List the location of the csv file(s)"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import dirname
from logging import debug
from timetracker.utils import yellow
from timetracker.msgs import str_init
from timetracker.cfg.cfg import Cfg


def cli_run_projects(fnamecfg, args):
    """Stop the timer and record this time unit"""
    cfg = Cfg(fnamecfg)
    cfg.set_cfg_global(args.global_config_file)
    run_projects(cfg)


def run_projects(cfg):  #, dirhome=None):
    """Stop the timer and record this time unit"""
    debug(yellow('RUNNING COMMAND PROJECTS'))
    proj_cfgs = cfg.cfg_glb.get_projects()
    if proj_cfgs:
        for proj, pcfg in proj_cfgs:
            print(f'    {proj:25} {dirname(dirname(pcfg))}')
    else:
        print(str_init(cfg.cfg_loc.filename))


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
