"""List the location of the csv file(s)"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import dirname
from logging import debug
from timetracker.utils import yellow
from timetracker.msgs import str_init
from timetracker.cfg.cfg_local import CfgProj
from timetracker.cfg.cfg_global import get_cfgglobal


def cli_run_projects(fnamecfg, args):
    """Stop the timer and record this time unit"""
    run_projects(fnamecfg, args.global_config_file)

def run_projects(fcfg_local, fcfg_global, dirhome=None):
    """Stop the timer and record this time unit"""
    # Get the starting time, if the timer is running
    debug(yellow('RUNNING COMMAND PROJECTS'))
    oglb = get_cfgglobal(fcfg_global, dirhome)
    proj_cfgs = oglb.get_projects()
    if proj_cfgs:
        for proj, pcfg in proj_cfgs:
            print(f'    {proj:25} {dirname(dirname(pcfg))}')
    else:
        cfg_loc = CfgProj(fcfg_local)
        print(str_init(cfg_loc.filename))


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
