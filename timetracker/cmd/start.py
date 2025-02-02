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
from timetracker.msgs import str_started
from timetracker.cfg.cfg_global import CfgGlobal


def cli_run_start(cfglocal, args):
    """Initialize timetracking on a project"""
    run_start(
        cfglocal,
        args)
        #args['project'],
        #args['csvdir'],
        #args['quiet'])

def run_start(cfglocal, args):
    """Initialize timetracking on a project"""
    debug('START: RUNNING COMMAND START')
    now = datetime.now()
    fin_start = cfglocal.get_filename_start()
    debug(f'START: exists({int(exists(fin_start))}) FILENAME({relpath(fin_start)})')
    # Print elapsed time, if timer was started
    cfglocal.prt_elapsed()
    # Set/reset starting time, if applicable
    forced = args.get('forced')
    if not exists(fin_start) or forced:
        cfglocal.mk_workdir()
        cfglocal_fname = cfglocal.get_filename_cfglocal()
        if not exists(cfglocal_fname):
            cfglocal.update_localini(args.get('project'), args.get('csvdir'))
            cfglocal.wr_cfg()
            cfg_global = CfgGlobal()
            chgd = cfg_global.add_proj(cfglocal.project, cfglocal.get_filename_cfglocal())
            if chgd:
                cfg_global.wr_cfg()
        with open(fin_start, 'w', encoding='utf8') as prt:
            prt.write(f'{now}')
            if not args.get('quiet'):
                print(f'Timetracker started '
                      f'{now.strftime("%a %I:%M %p")}: {now} '
                      f"for project '{cfglocal.project}' ID={cfglocal.name}")
            debug(f'  WROTE: {fin_start}')
    # Informational message
    elif not forced:
        print(str_started())
    else:
        print(f'Reseting start time to now({now})')
    debug(f'START: exists({int(exists(fin_start))}) FILENAME({relpath(fin_start)})')


    #dirtrk = kws['trksubdir']
    #if not exists(dirtrk):
    #    makedirs(dirtrk, exist_ok=True)
    #    absdir = abspath(dirtrk)
    #    print(f'Initialized timetracker trksubdir: {absdir}')
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
