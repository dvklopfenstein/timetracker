"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
#from os.path import abspath
#from os.path import relpath
from os.path import dirname
from logging import debug

##from timeit import default_timer
##$from datetime import timedelta
from datetime import datetime
#from timetracker.msgs import str_timed
#from timetracker.msgs import str_notrkrepo
from timetracker.msgs import str_init
from timetracker.utils import yellow
from timetracker.cfg.cfg_local  import CfgProj
from timetracker.csvfile import CsvFile


def cli_run_time(fnamecfg, args):
    """Initialize timetracking on a project"""
    run_time(
        fnamecfg,
        args.name,
        ##args.project,
        ##args['csvdir'],
        #args.force,
        #args.quiet
    )

def run_time(fnamecfg, uname, **kwargs):  #, name=None, force=False, quiet=False):
    """Initialize timetracking on a project"""
    debug(yellow('START: RUNNING COMMAND TIME'))
    #now = datetime.now()
    if not exists(fnamecfg):
        print(str_init(dirname(fnamecfg)))
        sys_exit(0)
    cfgproj = CfgProj(fnamecfg, dirhome=kwargs.get('dirhome'))
    fcsv = cfgproj.get_filename_csv(uname)
    if not exists(fcsv):
        _no_csv(fcsv, cfgproj, uname)
        return None
    ocsv = CsvFile(fcsv)
    #start_obj = cfgproj.get_timetime_obj(name)
    #fin_time = start_obj.filename
    ## Is this project tracked?
    ####if not exists(cfgproj_fname):
    ####    print(str_notrkrepo(dirname(dirname(cfgproj_fname))))
    ####    sys_exit(0)
    ## Print elapsed time, if timer was started
    #start_obj.prt_elapsed()
    ## Set/reset starting time, if applicable
    #if not exists(fin_time) or force:
    #    #cfgproj.mk_workdir()
    #    #cfgproj.update_localini(project, csvdir)
    #    #cfgproj.wr_cfg()
    #    #cfg_global = CfgGlobal()
    #    #chgd = cfg_global.add_proj(cfgproj.project, cfgproj.get_filename_cfgproj())
    #    #if chgd:
    #    #    cfg_global.wr_cfg()
    #    with open(fin_time, 'w', encoding='utf8') as prt:
    #        prt.write(f'{now}')
    #        if not quiet:
    #            print(f'Timetracker {"started" if not force else "reset to"} '
    #                  f'{now.strftime("%a %I:%M %p")}: {now} '
    #                  f"for project '{cfgproj.project}'")
    #        debug(f'  WROTE: {fin_time}')
    ## Informational message
    #elif not force:
    #    print(str_timeed())
    return None

def _no_csv(fcsv, cfgproj, uname):
    print(f'CSV file does not exist: {fcsv}')
    start_obj = cfgproj.get_starttime_obj(uname)
    start_obj.msg_fname01()


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
