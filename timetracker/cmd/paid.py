"""Stop the timer and record this time unit"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from logging import error
from timetracker.ntcsv import get_ntcsv
from timetracker.consts import FMTDT_H
from timetracker.csvrun import wr_csvline
from timetracker.cfg.utils import get_shortest_name
from timetracker.cmd.common import get_cfg
from timetracker.cmd.common import add_tag_billable
from timetracker.epoch.epoch import get_dt_at


def cli_run_paid(fnamecfg, args):
    """Stop the timer and record this time unit"""

    if not args.not_billable:
        add_tag_billable(args)
    _run_paid(
        fnamecfg,
        args.name,
        args.amount,
        paid_at=args.at,
        activity=args.activity,
        tags=args.tags)

def _run_paid(fnamecfg, uname, amount, paid_at=None, **kwargs):
    """Stop the timer and record this time unit"""
    cfg = get_cfg(fnamecfg)
    return run_paid(cfg.cfg_loc, uname, amount, paid_at, **kwargs)

def run_paid(cfgproj, uname, amount, paid_at=None, **kwargs):
    """Stop the timer and record this time unit"""
    fcsv = cfgproj.get_filename_csv(uname, kwargs.get('dirhome'))
    if fcsv is None:
        error('Not saving time interval; no csv filename was provided')
        return None

    paidtime = get_dt_at(paid_at, kwargs.get('now'), kwargs.get('defaultdt'))
    if paidtime is None:
        raise RuntimeError(f'NO PAID TIME FOUND in "{paid_at}"')

    # Append the timetracker file with this time unit
    csvline = wr_csvline(
        fcsv, paidtime, delta='',
        csvfields=get_ntcsv(f'PAID={amount}', kwargs.get('activity'), kwargs.get('tags')))
    print(f'PAID={amount} at {paidtime.strftime(FMTDT_H)} '
          f'appended to {get_shortest_name(fcsv)}')
    return {'fcsv':fcsv, 'csvline':csvline}


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
