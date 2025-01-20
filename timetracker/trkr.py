"""Command line interface (CLI) for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from timetracker.cfg import Cfg
from timetracker.cli import Cli
#from timetracker.recorder import Recorder


def main():
    """Command line interface (CLI) for timetracking"""
    cfg = Cfg()
    ini = cfg.get_cfgfile()
    print(f'CONF({ini})')
    cli = Cli(ini)
    args = cli.get_args()
    #rec = Recorder()


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
