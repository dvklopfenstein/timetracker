"""Connect all parts of the timetracker"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from logging import error
from timetracker.filemgr import FileMgr
##from timetracker.cfg import Cfg
from timetracker.cli import Cli
from timetracker.cmd.init import run_init
from timetracker.cmd.start import run_start
from timetracker.cmd.stop import run_stop
from timetracker.msgs import prt_started

fncs = {
    'init': run_init,
    'start': run_start,
    'stop': run_stop,
}


def main():
    """Connect all parts of the timetracker"""
    obj = TimeTracker()
    obj.run()


class TimeTracker:
    """Connect all parts of the timetracker"""
    # pylint: disable=too-few-public-methods

    def __init__(self):
        #self.cfg = Cfg()
        self.cli = Cli()
        self.args = self.cli.get_args()
        self.fmgr = FileMgr(**vars(self.args))

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
        start_file = self.fmgr.get_filename_start()
        if not exists(start_file):
            print('Run `trkr start` to begin timetracking '
                  f'for extant name({self.fmgr.name})')
        else:
            self.fmgr.prt_elapsed()
            prt_started()


    def _msg_init(self):
        self.cli.parser.print_help()
        print('')
        error('Run `trkr init` to initialize local timetracker')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
