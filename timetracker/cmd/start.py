"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
##from os.path import abspath
from os.path import relpath
##from os.path import join
from logging import debug

##from timeit import default_timer
##$from datetime import timedelta
from datetime import datetime
from timetracker.msgs import prt_started
from timetracker.cfg.cfg_global import CfgGlobal


def run_start(fmgr):
    """Initialize timetracking on a project"""
    debug('START: RUNNING COMMAND START')
    now = datetime.now()
    cfgproj = fmgr.cfg
    args = fmgr.kws
    fin_start = cfgproj.get_filename_start()
    debug(f'START: exists({int(exists(fin_start))}) FILENAME({relpath(fin_start)})')
    # Print elapsed time, if timer was started
    cfgproj.prt_elapsed()
    # Set/reset starting time, if applicable
    forced = fmgr.get('forced')
    if not exists(fin_start) or forced:
        cfgproj.mk_workdir()
        cfgproj_fname = cfgproj.get_filename_cfglocal()
        if not exists(cfgproj_fname):
            cfgproj.update_localini(args.get('project'), args.get('csvdir'))
            cfgproj.wr_cfg()
            cfg_global = CfgGlobal()
            cfg_global.add_proj(cfgproj.project, cfgproj.get_filename_cfglocal())
            cfg_global.wr_cfg()
        with open(fin_start, 'w', encoding='utf8') as prt:
            prt.write(f'{now}')
            if not fmgr.get('quiet'):
                print(f'Timetracker started '
                      f'{now.strftime("%a %I:%M %p")}: {now} '
                      f'for project {cfgproj.project}, ID {cfgproj.name}')
            debug(f'  WROTE: {fin_start}')
    # Informational message
    elif not forced:
        prt_started()
    else:
        print(f'Reseting start time to now({now})')
    debug(f'START: exists({int(exists(fin_start))}) FILENAME({relpath(fin_start)})')


    #dirtrk = kws['directory']
    #if not exists(dirtrk):
    #    makedirs(dirtrk, exist_ok=True)
    #    absdir = abspath(dirtrk)
    #    print(f'Initialized timetracker directory: {absdir}')
    #    fout_cfg = join(absdir, 'config')
    #    with open(fout_cfg, 'w', encoding='utf8') as ostrm:
    #        print('', file=ostrm)
    #        print(f'  WROTE: {relpath(fout_cfg)}')


#class CmdStart:
#    """Initialize a timetracker project"""
#    # pylint: disable=too-few-public-methods
#
#    def __init__(self, cfgfile):
#        self.cfgfile = cfgfile


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
