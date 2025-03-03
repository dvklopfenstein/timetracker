#!/usr/bin/env python3
"""Test the location of the csv file"""
# pylint: disable=duplicate-code

from os.path import exists
from logging import basicConfig
from logging import DEBUG
from logging import debug
from tempfile import TemporaryDirectory
from pytest import raises
from timetracker.utils import cyan
from timetracker.cfg.finder import CfgFinder
from timetracker.cmd.stop import get_ntcsv
from timetracker.cmd.stop import run_stop
from timetracker.cmd.time import run_time
from timetracker.cmd.cancel import run_cancel
from timetracker.cmd.csvupdate import run_csvupdate
from timetracker.cmd.report import run_report
from timetracker.cmd.start import run_start
from tests.pkgtttest.mkprojs import mk_projdirs
from tests.pkgtttest.mkprojs import findhome_str

basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'


def test_startat(project='pumpkin', username='carver'):
    """Test `trk start --at"""
    Obj(project, username, dircur='dirproj', dirgit01=True).run()
    Obj(project, username, dircur='dirdoc',  dirgit01=True).run()

class Obj:
    """Test the location of the csv file"""
    # pylint: disable=too-few-public-methods

    def __init__(self, project, username, dircur, dirgit01):
        self.project = project
        self.uname = username
        self.dircurattr = dircur
        self.dirgit01 = dirgit01

    def run(self):
        """Run init, start --at, stop"""
        debug(cyan(f'\n{"="*100}'))
        uname = self.uname
        with TemporaryDirectory() as tmphome:
            exp = mk_projdirs(tmphome, self.project, self.dirgit01)
            finder = CfgFinder(dircur=getattr(exp, self.dircurattr), trksubdir=None)
            cfgname = finder.get_cfgfilename()
            assert not exists(cfgname), findhome_str(exp.dirhome)

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
                run_time(cfgname, uname)
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
    test_startat()
