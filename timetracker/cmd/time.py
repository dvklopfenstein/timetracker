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
        unit=args.unit,
    )

def run_time(fnamecfg, uname, **kwargs):  #, name=None, force=False, quiet=False):
    """Initialize timetracking on a project"""
    debug(yellow('START: RUNNING COMMAND TIME'))
    if not exists(fnamecfg):
        print(str_init(dirname(fnamecfg)))
        sys_exit(0)
    cfgproj = CfgProj(fnamecfg, dirhome=kwargs.get('dirhome'))
    fcsv = cfgproj.get_filename_csv(uname)
    if not exists(fcsv):
        _no_csv(fcsv, cfgproj, uname)
        return None
    ocsv = CsvFile(fcsv)
    total_time = ocsv.read_totaltime()
    print(f'{total_time} or {total_time.total_seconds()/3600:.2f} hours')
    return total_time

def _no_csv(fcsv, cfgproj, uname):
    print(f'CSV file does not exist: {fcsv}')
    start_obj = cfgproj.get_starttime_obj(uname)
    start_obj.prtmsg_started01()


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
