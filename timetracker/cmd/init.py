"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from logging import debug
from timetracker.cfg.cfg_global import CfgGlobal


def cli_run_init(cfglocal, args):
    """initialize timetracking on a project"""
    run_init(
        cfglocal,
        args.project,
        args.csvdir,
        args.quiet)

def run_init(cfglocal, projectname, csvdir, quiet):
    """initialize timetracking on a project"""
    debug('INIT: RUNNING COMMAND INIT')
    debug(f'INIT: cfglocal:    {cfglocal}')
    debug(f'INIT: projectname: {projectname}')
    debug(f'INIT: csvdir:      {csvdir}')
    # 1. INITIALIZE LOCAL .timetracker PROJECT DIRECTORY
    cfglocal.mk_workdir(quiet)
    # pylint: disable=fixme
    # TODO: Check if cfg exists and needs to be updated
    cfglocal.update_localini(projectname, csvdir)
    debug(cfglocal.str_cfg())
    # 2. WRITE A LOCAL PROJECT CONFIG FILE: ./.timetracker/config
    cfglocal.wr_cfg()
    # 3. TODO: add `start_timetracker_*.txt` to the .gitignore if this is a git-managed repo
    # 4. WRITE A GLOBAL TIMETRACKER CONFIG FILE: ~/.timetrackerconfig, if needed
    cfg_global = CfgGlobal()
    chgd = cfg_global.add_proj(cfglocal.project, cfglocal.get_filename_cfglocal())
    if chgd:
        cfg_global.wr_cfg()
    ##cfg_global.write_update(args['project'], cfglocal.get_filename_cfglocal)



# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
