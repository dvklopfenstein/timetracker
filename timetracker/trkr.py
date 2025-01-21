"""Command line interface (CLI) for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from timetracker.cfg import Cfg
from timetracker.cli import Cli
from timetracker.init import run_init
#from timetracker.recorder import Recorder

fncs = {
    'init': run_init,
    #'start': run_start,
    #'stop': run_stop,
}


def main():
    """Command line interface (CLI) for timetracking"""
    cfg = Cfg()
    ini = cfg.get_cfgfile()
    print(f'CONF({ini})')
    cli = Cli(ini)
    args = cli.get_args()
    fncs[args.command](**vars(args))
    #rec = Recorder()


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
