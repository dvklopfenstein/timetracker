#!/usr/bin/env python3
"""Test running all commands when timetracker repo is uninitialized"""
# pylint: disable=duplicate-code

from logging import basicConfig
from logging import DEBUG
from logging import debug
from tempfile import TemporaryDirectory
from pytest import raises
from timetracker.utils import cyan
from timetracker.cmd.stop import run_stop
from timetracker.cmd.time import run_time_local
from timetracker.cmd.cancel import run_cancel
from timetracker.cmd.csvupdate import run_csvupdate
from timetracker.cmd.report import run_report
from timetracker.cmd.start import run_start
from timetracker.ntcsv import get_ntcsv
from tests.pkgtttest.runfncs import RunBase
from tests.pkgtttest.runfncs import proj_setup

basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'


def test_trk_cmdsall(project='pumpkin', username='carver'):
    """Test `trk start --at"""
    Obj(project, username, dircur='dirproj', dirgit01=True).run()
    Obj(project, username, dircur='dirdoc',  dirgit01=True).run()


class Obj(RunBase):
    """Test running all commands when timetracker repo is uninitialized"""
    # pylint: disable=too-few-public-methods

    def run(self):
        """Run init, start --at, stop"""
        debug(cyan(f'\n{"="*100}'))
        uname = self.uname
        with TemporaryDirectory() as tmphome:
            cfgname, _, _= proj_setup(tmphome, self.project, self.dircur, self.dirgit01)

            # DO NOT INIT

            # RUN COMMANDS WHEN timetracker repo IS NOT INIT
            # stop       Stop timetracking
            with raises(SystemExit) as excinfo:
                run_stop(cfgname, uname, get_ntcsv('Stop msg', None, None))
            assert excinfo.value.code == 0

            # cancel     cancel timetracking
            with raises(SystemExit) as excinfo:
                run_cancel(cfgname, uname)
            assert excinfo.value.code == 0

            # time       Report elapsed time
            with raises(SystemExit) as excinfo:
                run_time_local(cfgname, uname)
            assert excinfo.value.code == 0

            # report     Generate an report for all time units and include cumulative time
            with raises(SystemExit) as excinfo:
                run_report(cfgname, uname)
            assert excinfo.value.code == 0

            # csvupdate  Update values in csv columns containing weekday, am/pm, and duration
            with raises(SystemExit) as excinfo:
                run_csvupdate(cfgname, uname, None)
            assert excinfo.value.code == 0

            # start
            with raises(SystemExit) as excinfo:
                run_start(cfgname, uname)
            assert excinfo.value.code == 0


if __name__ == '__main__':
    test_trk_cmdsall()
