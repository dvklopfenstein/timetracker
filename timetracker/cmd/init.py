"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from logging import debug


def run_init(fmgr):
    """Initialize timetracking on a project"""
    debug('RUNNING COMMAND INIT')
    cfg = fmgr.cfg
    args = fmgr.kws
    # pylint: disable=fixme
    # TODO: Check if cfg exists and needs to be updated
    cfg.update_localini(args['project'], args['csvdir'])
    debug(cfg.str_cfg())
    fmgr.ini_workdir()
    cfg.wr_cfglocal()


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
