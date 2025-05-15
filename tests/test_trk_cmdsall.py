#!/usr/bin/env python3
"""Test running all commands when timetracker repo is uninitialized"""
# pylint: disable=duplicate-code

from logging import basicConfig
from logging import DEBUG
from logging import debug
from tempfile import TemporaryDirectory
from pytest import raises
from timetracker.utils import cyan
from timetracker.cfg.cfg_local import CfgProj
from timetracker.cmd.start import _run_start
from timetracker.cmd.start import run_start
from timetracker.cmd.stop import run_stop
from timetracker.cmd.hours import run_hours_local
from timetracker.cmd.cancel import run_cancel
from timetracker.cmd.none import run_none
from timetracker.cmd.csvupdate import run_csvupdate
from timetracker.cmd.report import run_report_cli
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
            fcfgloc, _, fnms = proj_setup(tmphome, self.project, self.dircur, self.dirgit01)
            cfg_proj = CfgProj(fcfgloc)
            print(fnms)

            # DO NOT INIT

            # RUN COMMANDS WHEN timetracker repo IS NOT INIT
            # stop       Stop timetracking
            assert run_stop(cfg_proj, uname, get_ntcsv('Stop msg', None, None)) is None
            #assert set(ret.values()) == {None}

            assert run_none(cfg_proj, uname) is None

            # cancel     cancel timetracking
            assert run_cancel(cfg_proj, uname) is None

            # time       Report elapsed time
            assert run_hours_local(cfg_proj, uname) is None

            # report     Generate an report for all time units and include cumulative time
            assert run_report_cli(cfg_proj, uname) is None

            # csvupdate  Update values in csv columns containing weekday, am/pm, and duration
            with raises(SystemExit) as excinfo:
                run_csvupdate(fcfgloc, uname, None)
            assert excinfo.value.code == 0

            # start
            with raises(SystemExit) as excinfo:
                _run_start(fcfgloc, uname)
            assert excinfo.value.code == 0

            # start
            assert run_start(cfg_proj, uname) is None


if __name__ == '__main__':
    test_trk_cmdsall()
