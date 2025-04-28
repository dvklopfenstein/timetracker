"""Report the total time in hours spent on a project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
from collections import namedtuple
from logging import debug
from datetime import timedelta
from itertools import groupby
from timetracker.cfg.cfg import Cfg
from timetracker.cfg.utils import get_filename_globalcfg
from timetracker.cfg.cfg_global import CfgGlobal
from timetracker.cfg.doc_local import get_docproj
#from timetracker.cmd.common import get_fcsv
from timetracker.utils import yellow
from timetracker.csvrun import chk_n_convert
from timetracker.csvfile import CsvFile
from timetracker.csvget import get_csvs_local_uname
from timetracker.csvget import get_csvs_global_uname
from timetracker.msgs import str_init0
from timetracker.msgs import str_tostart_epoch
from timetracker.projects import get_ntcsvproj01

NTCSVS = namedtuple('RdCsvs', 'results errors ntcsvs')

def cli_run_hours(fnamecfg, args):
    """Report the total time in hours spent on a project"""
    #print(f'ARGS FOR HOURS: {fnamecfg} {args}')
    if args.fcsv and exists(args.fcsv):
        ntd = get_ntcsvproj01(fnamecfg, args.fcsv, args.name)
        if ntd:
            return _rpt_hours_uname1(ntd)
        return None
    #print(f'ARGS FOR HOURS: {fnamecfg} {args}')
    cfg = Cfg(fnamecfg)
    return run_hours(cfg, args.name, args.run_global, args.global_config_file)

def run_hours(cfg, uname, get_global=False, global_config_file=None, dirhome=None):
    """Report the total time in hours spent on project(s)"""
    #print('RUN COMMAND HOURS')
    if get_global or not exists(cfg.cfg_loc.filename):
        #print('RUN HOURS GLOBAL')
        if cfg.cfg_glb is None:
            docglb = get_docproj(cfg.cfg_loc.filename)
            fcfg_gdoc = None if not docglb else docglb.global_config_filename
            fglb = get_filename_globalcfg(dirhome, global_config_file, fcfg_gdoc)
            if not exists(fglb):
                print(str_init0())
                sys_exit(0)
            cfg.cfg_glb = CfgGlobal(fglb)
        return run_hours_global(cfg.cfg_glb, uname)  # RdCsvs: results errors ntcsvs
    #print('RUN HOURS GLOBAL')
    ret = run_hours_local(cfg.cfg_loc, uname, dirhome)
    if ret is None:
        print(str_tostart_epoch())
    return ret  # RdCsv: results error

def run_hours_global(cfg_global, uname):
    """Report the total hours spent on all projects by uname"""
    assert cfg_global is not None
    #print('RUN HOURS GLOBAL START')
    if (projects := cfg_global.get_projects()):
        ntcsvs = get_csvs_global_uname(projects, uname)
        ntres = _rpt_hours_projs_uname1(ntcsvs, uname)
        return ntres  # RdCsvs: results errors ntcsvs
    return None

def run_hours_local(cfg_proj, uname, dirhome=None):
    """Report the total time in hours spent on a project"""
    debug(yellow('RUNNING COMMAND HOURS local'))
    ntd = get_csvs_local_uname(cfg_proj.filename, uname, dirhome)
    return _rpt_hours_uname1(ntd)  # nt

#def run_hours_global(fnamecfg, uname, **kwargs):  #, name=None, force=False, quiet=False):
#    """Report the total time spent on all projects"""

def _rpt_hours_uname1(ntd):
    if ntd and (nt_total_time := _get_total_time(ntd.fcsv)):
        assert ntd.username is not None, ntd
        if nt_total_time.results is not None:
            in_msg = f'project {ntd.project} in {ntd.fcsv}' if ntd.project else ntd.fcsv
            print(f'{_get_hours_str(nt_total_time.results)} by {ntd.username} in {in_msg}')
            return nt_total_time
    return None

def _rpt_hours_projs_uname1(ntcsvs, username, uname_len=8):
    assert username is not None
    total_time = timedelta()
    print('    hours username project')
    print('  ------- -------- ----------------------')
    # ntcsvs:     fcsv project username
    # ntcsvtimes: results errors fcsv
    itr = ((_get_total_time(nt.fcsv), nt) for nt in ntcsvs)
    rd01 = {k: list(g) for k, g in groupby(itr, key=lambda t: t[0].results is not None)}
    errnts = rd01.get(False)
    if (rdnts := rd01.get(True)):
        for nttime, ntcsv in rdnts:
            if nttime.results:
                total_time += nttime.results
                print(f'{_get_hours_str(nttime.results)} {username:{uname_len}} {ntcsv.project}')
        _rpt_errs_csvread(errnts)
        print(f'{_get_hours_str(total_time)} {username:{uname_len}} Total hours for all projects')
        return NTCSVS(results=total_time, errors=errnts, ntcsvs=rdnts)
    _rpt_errs_csvread(errnts)
    return None

def _rpt_errs_csvread(nts):
    if not nts:
        return
    #if nts:
    #    print('CSV files not read:')
    for ntrd, ntcsv in nts:
        assert ntrd.results is None
        errtxt = ntrd.error.args[1]
        #if True: # errtxt != 'No such file or directory':
        print(f'INFO: {errtxt}: {ntrd.error.filename}')
        assert ntcsv.fcsv
        #print(f'{ntd[0].error} {ntd}')

#def _rpt_hours_uname0(ntd):
#    assert uname is not None
#    total_time = _get_total_time(ntd.fcsv)
#    print(f'{_get_hours_str(total_time)} in project {ntd.project}')
#    return total_time

def _get_hours_str(total_time):
    return f'{total_time.total_seconds()/3600:10.3f}'

def _get_total_time(fcsv):
    chk_n_convert(fcsv)
    ocsv = CsvFile(fcsv)
    return ocsv.read_totaltime_all()


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
