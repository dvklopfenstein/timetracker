#!/usr/bin/env python3
"""Test report command"""

from os.path import exists
from tempfile import TemporaryDirectory
from logging import basicConfig
from timetracker.utils import yellow
from timetracker.ntcsv import NTCSV
from timetracker.cfg.cfg import Cfg
from timetracker.cmd.report import run_report_cli
from timetracker.cmd.init import run_init
from timetracker.cmd.start import run_start
from timetracker.cmd.stop import run_stop
from timetracker.cmd.none import run_none
from timetracker.epoch.text import get_data_formatted
from tests.pkgtttest.runprojs import RunProjs
from tests.pkgtttest.runfncs import get_cfgproj


USERPROJS = {
    ('david'  , 'shepherding'): ([('Mon', 'Fri',  '5am',        '6am')],  5.0),
    ('lambs'  , 'grazing'):     ([('Mon', 'Fri',  '5am',        '7am')], 10.0),
    ('lambs'  , 'sleeping'):    ([('Mon', 'Fri',  '7pm',       '11pm')], 20.0),
    ('goats'  , 'grazing'):     ([('Mon', 'Fri',  '5am',        '8am')], 15.0),
    ('goats'  , 'sleeping'):    ([('Mon', 'Fri',  '6:59pm', '11:59pm')], 25.0),
    ('lions'  , 'hunting'):     ([('Mon', 'Fri',  '5am',        '9am')], 20.0),
    ('jackels', 'scavenging'):  ([('Mon', 'Fri',  '5am',       '10am')], 25.0),
}

def test_report():
    """Test report command for many timeslots and many users"""
    with TemporaryDirectory() as tmproot:
        basicConfig()
        orun = RunProjs(tmproot, USERPROJS)
        orun.run_setup()
        for (uname, proj), pobj in orun.prj2mgrprj.items():
            print(yellow(f'\nUNAME({uname}) PROJECT({proj})'))
            ntcsv = run_report_cli(pobj.cfg.cfg_loc, uname, dirhome=orun.dirhome)
            assert ntcsv.error is None
            assert len(ntcsv.results) == 5
            # test pnum
            for ntd in get_data_formatted(ntcsv.results):
                assert 'Sum' not in ntd._fields
            for ntd in get_data_formatted(ntcsv.results, pnum=True):
                assert 'Sum' in ntd._fields

def test_report_nocsv(username='rando'):
    """Test the report command when there is no csv"""
    with TemporaryDirectory() as tmproot:
        cfgproj = get_cfgproj(tmproot)
        dirgit = None

        tobj = RunTest(cfgproj, tmproot, username)

        print(yellow('\nTEST: `trk report` when there is NO timetracker repo'))
        ntcsv = tobj.run_report()
        assert ntcsv is None

        print(yellow('\nTEST: `trk report` when there IS a timetracker repo'))
        cfg = Cfg(cfgproj.filename)
        run_init(cfg, dirgit)
        ntcsv = tobj.run_report()
        tobj.chk_filenotfounderror(ntcsv)

        print(yellow('\nTEST: `trk report` when timetracker is started, but no csv file yet'))
        tobj.start_x2()
        ntcsv = tobj.run_report()
        tobj.chk_filenotfounderror(ntcsv)

        print(yellow('\nTEST: `trk report` after timetracker is stopped'))
        csvfields = NTCSV(message='Testing writing csv', activity='', tags='')
        run_stop(cfgproj, username, csvfields)
        ntcsv = tobj.run_report()
        assert ntcsv.error is None

        print(yellow('\nTEST: `trk`'))
        assert run_none(cfgproj, username) is not None


class RunTest:
    """Test cases include when there is no csv file"""

    def __init__(self, cfgproj, tmproot, username):
        self.cfgproj = cfgproj
        self.tmproot = tmproot
        self.username = username

    def run_report(self):
        """Run `run_report`"""
        return run_report_cli(self.cfgproj, self.username, dirhome=self.tmproot)

    def start_x2(self):
        """Run `trk start` twice"""
        ostrt1 = run_start(self.cfgproj, self.username)
        assert exists(ostrt1.filename)
        assert ostrt1.read_starttime() is not None
        ostrt2 = run_start(self.cfgproj, self.username)
        assert ostrt1.read_starttime() == ostrt2.read_starttime()
        return ostrt1

    def chk_filenotfounderror(self, ntcsv):
        """Test to see that a proper FileNotFoundError is produced"""
        assert ntcsv.results is None
        assert ntcsv.error.errno == 2
        assert ntcsv.error.strerror == 'No such file or directory'
        # /tmp/tmp4mdo8fdh/timetracker_tmp4mdo8fdh_rando.csv
        fcsv = self.cfgproj.get_filename_csv(self.username, dirhome=self.tmproot)
        assert ntcsv.error.filename == fcsv, ('ACT != EXP\n'
            f'ACT({ntcsv.error.filename})\n'
            f'EXP({fcsv})\n')

if __name__ == '__main__':
    test_report()
    test_report_nocsv()
