"""List the location of the csv file(s)"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from logging import debug
from timetracker.utils import yellow
from timetracker.cfg.cfg_local  import CfgProj
from timetracker.cfg.cfg_global import CfgGlobal
from timetracker.msgs import str_init


def cli_run_csv(fnamecfg, args):
    """Stop the timer and record this time unit"""
    run_csv(
        fnamecfg,
        args.name)

def run_csv(fnamecfg, uname, dirhome=None):
    """Stop the timer and record this time unit"""
    # Get the starting time, if the timer is running
    debug(yellow('RUNNING COMMAND CSV'))
    if not exists(fnamecfg):
        print(str_init(fnamecfg))
    cfgproj = CfgProj(fnamecfg, dirhome=dirhome)

    # List location of the timetracker file with this time unit
    if uname == 'all':
        _get_csv_proj_all(cfgproj)
    else:
        _get_csv_proj_user(cfgproj, uname)

def _get_csv_proj_user(cfgproj, uname):
    fcsv = cfgproj.get_filename_csv(uname)
    if fcsv is not None:
        print(f'CSV exists({int(exists(fcsv))}) {fcsv}')

def _get_csv_proj_all(cfgproj):
    fcsvs = cfgproj.get_project_csvs()
    for fcsv in fcsvs:
        if fcsv is not None:
            print(f'CSV exists({int(exists(fcsv))}) {fcsv}')

def _run_cfg_global(dirhome):
    cfg_global = CfgGlobal(dirhome)
    assert cfg_global


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
