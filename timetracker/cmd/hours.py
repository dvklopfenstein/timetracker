"""Report the total time in hours spent on a project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from logging import debug
from timetracker.cmd.common import get_cfg
from timetracker.cmd.common import get_fcsv
from timetracker.utils import yellow
from timetracker.csvrun import chk_n_convert
from timetracker.csvfile import CsvFile


def cli_run_hours(fnamecfg, args):
    """Report the total time in hours spent on a project"""
    if args.input and exists(args.input):
        _rpt_hours(args.input)
        return
    run_hours_local(
        fnamecfg,
        args.name,
    )
    #if args.global:
    #    run_hours_global(
    #    )

def run_hours_local(fnamecfg, uname, dirhome=None):  #, name=None, force=False, quiet=False):
    """Report the total time in hours spent on a project"""
    debug(yellow('RUNNING COMMAND TIME'))
    cfg = get_cfg(fnamecfg)
    fcsv = get_fcsv(cfg, uname, dirhome)
    return _rpt_hours(fcsv) if fcsv is not None else None

#def run_hours_global(fnamecfg, uname, **kwargs):  #, name=None, force=False, quiet=False):
#    """Report the total time spent on all projects"""

def _rpt_hours(fcsv):
    chk_n_convert(fcsv)
    ocsv = CsvFile(fcsv)
    total_hours = ocsv.read_totaltime_all()
    print(f'{total_hours} H:M:S or {total_hours.total_seconds()/3600:.3f} hours')
    return total_hours


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
