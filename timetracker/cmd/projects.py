"""List the location of the csv file(s)"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

#from os.path import dirname
#from os.path import exists
from logging import debug
from timetracker.utils import yellow
from timetracker.cfg.cfg import Cfg
#from timetracker.cfg.utils import get_filename_globalcfg
#from timetracker.cfg.cfg_global import CfgGlobal
#from timetracker.msgs import str_init


def cli_run_projects(fnamecfg, args):
    """Stop the timer and record this time unit"""
    run_projects(fnamecfg, args.global_config_file)

def run_projects(fcfg_local, fcfg_global, dirhome=None):
    """Stop the timer and record this time unit"""
    # Get the starting time, if the timer is running
    debug(yellow('RUNNING COMMAND PROJECTS'))
    cfg = Cfg(fcfg_local)  #### , fcfg_global, dirhome)
    if cfg.needs_init(fcfg_global, dirhome):
        return
    return
    #filename_globalcfg = get_filename_globalcfg(dirhome) if file is None else file
    #if not exists(filename_globalcfg):
    #    print(str_init(fcfg_local))
    #    return
    #cfg_global = CfgGlobal(filename_globalcfg)
    #projects = cfg_global.get_projects()
    #if projects is None:
    #    print(str_init(print(str_init(fcfg_local))))
    #for proj, fcfgloc in sorted(projects):
    #    print(f'{proj:26} {dirname(dirname(fcfgloc))}')


    #cfg = Cfg(fcfg_local, fcfg_global)

#    if not exists(fnamecfg):
#        run_projects_global(uname)
#    cfgproj = CfgProj(fnamecfg, dirhome=dirhome)
#
#    # List location of the timetracker file with this time unit
#    if uname == 'all':
#        _get_proj_all(cfgproj)
#    else:
#        _get_proj_user(cfgproj, uname)
#
#def _get_proj_user(cfgproj, uname):
#    fcsv = cfgproj.get_filename_csv(uname)
#    if fcsv is not None:
#        print(f'CSV exists({int(exists(fcsv))}) {fcsv}')
#
#def _get_proj_all(cfgproj, dirhome):
#    fcsvs = cfgproj.get_project_csvs(dirhome)
#    for fcsv in fcsvs:
#        if fcsv is not None:
#            print(f'CSV exists({int(exists(fcsv))}) {fcsv}')
#
#def _run_cfg_global(dirhome):
#    cfg_global = CfgGlobal(dirhome)
#    assert cfg_global
#
#
#def run_projects_global(uname):
#    print(filename_globalcfg)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
