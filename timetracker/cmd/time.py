"""Report the total time spent on a project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from logging import debug
from timetracker.cmd.common import get_fcsv
from timetracker.utils import yellow
from timetracker.csvold import CsvFile


def cli_run_time(fnamecfg, args):
    """Report the total time spent on a project"""
    if args.input and exists(args.input):
        _rpt_time(args.input)
        return
    run_time(
        fnamecfg,
        args.name,
        unit=args.unit,
    )

def run_time(fnamecfg, uname, **kwargs):  #, name=None, force=False, quiet=False):
    """Report the total time spent on a project"""
    debug(yellow('RUNNING COMMAND TIME'))
    fcsv = get_fcsv(fnamecfg, uname, kwargs.get('dirhome'))
    return _rpt_time(fcsv) if fcsv is not None else None

def _rpt_time(fcsv):
    ocsv = CsvFile(fcsv)
    total_time = ocsv.read_totaltime()
    print(f'{total_time} H:M:S or {total_time.total_seconds()/3600:.3f} hours')
    return total_time

def _no_csv(fcsv, cfgproj, uname):
    #print(f'CSV file does not exist: {fcsv}')
    start_obj = cfgproj.get_starttime_obj(uname)
    start_obj.prtmsg_started_csv(fcsv)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
