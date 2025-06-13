"""Show information regarding the location of the csv files"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from timetracker.cfg.cfg import Cfg
from timetracker.csvget import get_csv_local_uname
from timetracker.cmd.common import str_uninitialized


def cli_run_csv(fnamecfg, args):
    """Show information regarding the location of the csv files"""
    cfg = Cfg(fnamecfg)
    run_csv(
        cfg,
        args.name,
        args.run_global,
        args.all)
        #fcfg_global=args.global_config_file)

##def run_csv(fnamecfg, dircsv, project, dirhome=None, fcfg_global=None):
def run_csv(cfg, uname, get_global, get_all, dirhome=None):  #, **kwargs):
    """Initialize timetracking on a project"""
    #fcfg_global = kwargs.get('fcfg_global')
    if not get_global and not get_all:
        print(f'00 {get_global=} {get_all=}')
        _get_csv_local_uname(cfg.cfg_loc, uname, dirhome)
        return
    if not get_global and     get_all:
        print(f'01 {get_global=} {get_all=}')
        return
    if     get_global and not get_all:
        print(f'10 {get_global=} {get_all=}')
        _get_csvs_global_uname(cfg, uname, dirhome)
        return
    if     get_global and     get_all:
        print(f'11 {get_global=} {get_all=}')
        return
    #cfgproj = _run_csvlocate_local(fnamecfg, dircsv, project)
    #debug(cfgproj.get_desc("new"))
    #fcfg_doc = get_docproj(cfgproj.filename) if cfgproj else None
    #dirhome = get_filename_globalcfg(dirhome, fcfg_global, fcfg_doc)
    #assert dirhome

def _get_csv_local_uname(cfgproj, uname, dirhome=None):
    if str_uninitialized(cfgproj.filename):
        sys_exit(0)
    res = get_csv_local_uname(cfgproj.filename, uname, dirhome)
    print(res)

def _get_csvs_global_uname(cfg, uname, dirhome=None):
    assert cfg
    assert uname
    assert dirhome


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
