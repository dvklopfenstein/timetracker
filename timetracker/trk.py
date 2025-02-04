"""Connect all parts of the timetracker"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import getcwd
from os.path import exists
#from logging import error

from logging import basicConfig
from logging import DEBUG
from logging import debug
###from logging import INFO

from timetracker.cfg.cfg_local  import CfgProj
from timetracker.cli import Cli
from timetracker.msgs import str_started
from timetracker.cmd.init      import cli_run_init
from timetracker.cmd.start     import cli_run_start
from timetracker.cmd.stop      import cli_run_stop
from timetracker.cmd.csvupdate import cli_run_csvupdate

fncs = {
    'init'     : cli_run_init,
    'start'    : cli_run_start,
    'stop'     : cli_run_stop,
    'csvupdate': cli_run_csvupdate,
}


def main():
    """Connect all parts of the timetracker"""
    basicConfig(level=DEBUG)
    obj = TimeTracker()
    obj.run()

    ##cfg_local = CfgProj()
    ##cli = Cli(cfg_local)
    ##args = cli.get_args_cli()


class TimeTracker:
    """Connect all parts of the timetracker"""
    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.cli = Cli()
        self.cfg_local = CfgProj()
        self.cfg_local.workdir = self.cli.finder.get_dirtrk()
        ##self.args = self.cli.get_args_cli()
        self.args = self.cli.args

    def run(self):
        """Run timetracker"""
        debug(f'TIMETRACKER ARGS: {self.args}')
        if self.args.command is not None:
            ##self.cfg_local = CfgProj()
            fncs[self.args.command](self.cfg_local, self.args)
        else:
            self._cmd_none()

    def _cmd_none(self):
        if not exists(self.args.trksubdir):
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
