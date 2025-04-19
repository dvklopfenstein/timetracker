"""Report the total time in hours spent on a project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
from logging import debug
from timetracker.cfg.cfg import Cfg
from timetracker.cfg.cfg_global import CfgGlobal
#from timetracker.cmd.common import get_fcsv
from timetracker.utils import yellow
from timetracker.csvrun import chk_n_convert
from timetracker.csvfile import CsvFile
from timetracker.cfg.utils import get_filename_globalcfg
from timetracker.msgs import str_init0
from timetracker.projects import get_csvs_username
from timetracker.projects import get_ntcsvproj01
from timetracker.projects import get_ntcsvproj11


def cli_run_hours(fnamecfg, args):
    """Report the total time in hours spent on a project"""
    #print(f'ARGS FOR HOURS: {args}')
    if args.input and exists(args.input):
        ntd = get_ntcsvproj01(fnamecfg, args.input, args.name)
        if ntd:
            _rpt_hours_uname1(ntd)
        return
    cfg = Cfg(fnamecfg)
    run_hours(cfg, args.name, args.run_global, args.global_config_file)
    #if args.global:
    #    run_hours_global(
    #    )

def run_hours(cfg, uname, get_global=False, global_config_file=None, dirhome=None):
    """Report the total time in hours spent on project(s)"""
    #print('RUN HOURS START')
    if get_global or not exists(cfg.cfg_loc.filename):
        #print('RUN HOURS GLOBAL')
        if cfg.cfg_glb is None:
            fglb = get_filename_globalcfg(dirhome, global_config_file)
            if not exists(fglb):
                print(str_init0())
                sys_exit(0)
            cfg.cfg_glb = CfgGlobal(fglb)
        run_hours_global(cfg.cfg_glb, uname)
    else:
        #print('RUN HOURS LOCAL')
        run_hours_local(cfg.cfg_loc, uname, dirhome)

def run_hours_global(cfg_global, uname):
    """Report the total hours spent on all projects by uname"""
    assert cfg_global is not None
    #print('RUN HOURS GLOBAL START')
    if (projects := cfg_global.get_projects()):
        _rpt_hours_projs_uname1(get_csvs_username(projects, uname), uname)

def run_hours_local(cfg_proj, uname, dirhome=None):
    """Report the total time in hours spent on a project"""
    debug(yellow('RUNNING COMMAND TIME'))
    ntd = get_ntcsvproj11(cfg_proj.filename, uname, dirhome)
    return _rpt_hours_uname1(ntd) if ntd is not None else None

#def run_hours_global(fnamecfg, uname, **kwargs):  #, name=None, force=False, quiet=False):
#    """Report the total time spent on all projects"""

def _rpt_hours_uname1(ntd):
    assert ntd.username is not None
    total_time = _get_total_time(ntd.fcsv)
    print(f'{_get_hours_str(total_time)} by {ntd.username:14} in project {ntd.project}')
    return total_time

def _rpt_hours_projs_uname1(ntcsvs, username, uname_len=8):
    assert username is not None
    print('    hours        username projects')
    print('  -------------- -------- ----------------------')
    for ntd in ntcsvs:
        if (total_time := _get_total_time(ntd.fcsv)):
            print(f'{_get_hours_str(total_time)} {username:{uname_len}} {ntd.project}')

#def _rpt_hours_uname0(ntd):
#    assert uname is not None
#    total_time = _get_total_time(ntd.fcsv)
#    print(f'{_get_hours_str(total_time)} in project {ntd.project}')
#    return total_time

def _get_hours_str(total_time):
    return f'{total_time.total_seconds()/3600:9.3f} hours '

def _get_total_time(fcsv):
    chk_n_convert(fcsv)
    ocsv = CsvFile(fcsv)
    return ocsv.read_totaltime_all()


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
