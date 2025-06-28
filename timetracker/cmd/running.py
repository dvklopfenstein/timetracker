"""List the location of the csv file(s)"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import dirname
from timetracker.cfg.cfg import Cfg
from timetracker.cfg.doc_local import get_docproj
from timetracker.cmd.common import str_uninitialized
from timetracker.consts import FMTDT_H


def cli_run_running(fnamecfg, args):
    """Stop the timer and record this time unit"""
    cfg = Cfg(fnamecfg)
    cfg.set_cfg_global()
    run_running(cfg, args.name, args.verbose)


def run_running(cfg, uname, verbose=False):
    """Show the running listed in the global config"""
    cfg_glb = cfg.cfg_glb
    if not str_uninitialized(cfg_glb.filename):
        _show_running(cfg_glb, uname, verbose)

def _show_running(cfg_glb, uname, verbose):
    """Show the running listed in the global config"""
    proj_cfgs = cfg_glb.get_projects()
    if proj_cfgs:
        runcnt = 0
        for _, pcfg in proj_cfgs:
            if (doc := get_docproj(pcfg)) is not None and \
               (startobj := doc.get_startobj(uname)) is not None and \
                startobj.started():
                if (dta := startobj.read_starttime()):
                    print(startobj.str_elapsed_hms(
                          startobj.hms_from_startfile(dta),
                          f'Timer started on {dta.strftime(FMTDT_H)} and running'))
                    if verbose:
                        print(f'    {dirname(dirname(pcfg))}\n')
                    runcnt += 1
                else:
                    print(f'ERROR: NO TIME FOUND '
                          f'FOR USERNAME({startobj.name}) '
                          f'FOR PROJECT({startobj.project}) '
                          f'IN:\n    {startobj.filename}')
        print(f'{runcnt} of {len(proj_cfgs)} projects have running timers; '
              f'listed in: {cfg_glb.filename}')
    else:
        print(f'There are no running in {cfg_glb.filename}')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
