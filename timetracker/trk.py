"""Connect all parts of the timetracker"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import getcwd
from os.path import exists
#from logging import error

#from logging import basicConfig
#from logging import DEBUG
###from logging import INFO

from timetracker.filemgr import FileMgr
from timetracker.cfg.cfg_global import CfgGlobal
from timetracker.cfg.cfg_local import CfgProj
from timetracker.cli import Cli
from timetracker.msgs import str_started
from timetracker.cmd.init import run_init
from timetracker.cmd.start import run_start
from timetracker.cmd.stop import run_stop
from timetracker.cmd.csvupdate import run_csvupdate

fncs = {
    'init': run_init,
    'start': run_start,
    'stop': run_stop,
    'csvupdate': run_csvupdate,
}


def main():
    """Connect all parts of the timetracker"""
    #basicConfig(level=DEBUG)
    obj = TimeTracker()
    obj.run()


class TimeTracker:
    """Connect all parts of the timetracker"""
    # pylint: disable=too-few-public-methods

    def __init__(self):
        cfg_global = CfgGlobal()
        cfg_local = CfgProj()
        self.cfg_local = cfg_local
        self.cli = Cli(cfg_local)
        self.args = self.cli.get_args_cli()
        self.fmgr = FileMgr(cfg_local, cfg_global, **vars(self.args))

    def run(self):
        """Run timetracker"""
        if self.args.command is not None:
            fncs[self.args.command](self.fmgr)
        else:
            self._cmd_none()

    def _cmd_none(self):
        if not self.fmgr.exists_workdir():
            self._msg_init()
            return
        # Check for start time
        start_file = self.cfg_local.get_filename_start()
        if not exists(start_file):
            print('Run `trk start` to begin timetracking')
        else:
            self.cfg_local.prt_elapsed()
            print(str_started())

    def _msg_init(self):
        self.cli.parser.print_help()
        print('\nRun `trk init` to initialize time-tracking '
              f'for the project in {getcwd()}')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
