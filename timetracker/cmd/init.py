"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from logging import debug
from timetracker.cfg.cfg_global import CfgGlobal


def run_init(fmgr):
    """Initialize timetracking on a project"""
    debug('INIT: RUNNING COMMAND INIT')
    cfg_local = fmgr.cfg
    args = fmgr.kws
    # 1. INITIALIZE A LOCAL .timetracker PROJECT DIRECTORY
    fmgr.ini_workdir()
    # pylint: disable=fixme
    # TODO: Check if cfg exists and needs to be updated
    cfg_local.update_localini(args['project'], args['csvdir'])
    debug(cfg_local.str_cfg())
    # 2. WRITE A LOCAL PROJECT CONFIG FILE: ./.timetracker/config
    cfg_local.wr_cfg()
    # 3. WRITE A GLOBAL TIMETRACKER CONFIG FILE: ~/.timetrackerconfig
    cfg_global = CfgGlobal()
    ##cfg_global.write_update(args['project'], cfg_local.get_filename_cfglocal)



# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
