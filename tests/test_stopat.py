#!/usr/bin/env python3
"""Test `trk stop --at`"""

from os import system
from os.path import exists
from os.path import join
from io import StringIO
#from logging import basicConfig
#from logging import DEBUG
from logging import debug
from tempfile import TemporaryDirectory
from csv import writer
from timetracker.utils import cyan
from timetracker.utils import yellow
from timetracker.ntcsv import get_ntcsv
from timetracker.cmd.init import run_init_test
from timetracker.cmd.start import run_start
from timetracker.cmd.stop import run_stop
from tests.pkgtttest.dts import DT2525
from tests.pkgtttest.runfncs import RunBase
from tests.pkgtttest.runfncs import proj_setup

#basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'


def test_stopat(project='pumpkin', username='carver'):
    """Test `trk stop --at"""
    _run(Obj(project, username, dircur='dirproj', dirgit01=True))
    #_run(Obj(project, username, dircur='dirdoc',  dirgit01=True))

def _run(obj):
    # Test researcher-entered datetime stoptimes
    # pylint: disable=line-too-long
    obj.chk('4am',                   'Mon,AM,2525-01-01 00:00:00,Mon,AM,2525-01-01 04:00:00,4:00:00,"A,B,C",,')
    return
    # pylint: disable=unreachable
    obj.chk("2025-02-19 17:00:00",   '2025-02-19 17:00:00')
    obj.chk("2025-02-19 05:00:00 pm",'2025-02-19 17:00:00')
    obj.chk("02-19 17:00:00",        '2525-02-19 17:00:00')
    obj.chk("02-19 05:00:00 pm",     '2525-02-19 17:00:00')
    obj.chk("02-19 5pm",             '2525-02-19 17:00:00')
    obj.chk("02-19 5:00 pm",         '2525-02-19 17:00:00')
    obj.chk("2-19 5:30 pm",          '2525-02-19 17:30:00')
    # Test researcher-entered datetime timedeltas
    obj.chk("30 minutes", '2525-01-01 00:30:00')
    obj.chk("30 min",     '2525-01-01 00:30:00')
    obj.chk("30min",      '2525-01-01 00:30:00')
    obj.chk("00:30:00",   '2525-01-01 00:30:00')
    obj.chk("30:00",      '2525-01-01 00:30:00')
    obj.chk("4 hours",    '2525-01-01 04:00:00')
    obj.chk("04:00:00",   '2525-01-01 04:00:00')
    obj.chk("4:00:00",    '2525-01-01 04:00:00')


class Obj(RunBase):
    """Test `trk stop --at`"""
    # pylint: disable=too-few-public-methods

    def _run(self, stop_at, tmphome, dircsv=None):
        """Run init, stop --at, stop"""
        cfgname, _, exp = proj_setup(tmphome, self.project, self.dircur, self.dirgit01)
        # pylint: disable=unused-variable
        cfgp, _ = run_init_test(cfgname, dircsv, self.project, exp.dirhome, quiet=True)  # cfgg
        fin_start = run_start(cfgname, self.uname, now=DT2525, defaultdt=DT2525)
        assert exists(fin_start)
        csvfields = get_ntcsv("A,B,C", None, None)
        fcsv, act = run_stop(cfgname, self.uname, csvfields,
                             dirhome=tmphome, stop_at=stop_at, defaultdt=DT2525)
        assert fcsv == join(tmphome, 'proj/pumpkin/timetracker_pumpkin_carver.csv')
        assert exists(fcsv)
        system(f'cat {fcsv}')
        #findhome(tmphome)
        return act

    def chk(self, stop_at, exp_str):
        """Run stop --at and check value"""
        print(yellow(f'\nTEST: stop={stop_at:22} EXP={exp_str}'))
        debug(cyan(f'\n{"="*100}'))
        debug(cyan(f'RUN(stop_at={stop_at})'))
        with TemporaryDirectory() as tmphome:
            act_list = self._run(stop_at, tmphome)
            act_str = self._get_actstr(act_list)
            assert act_str == exp_str, f'ERROR({stop_at}))\nACT: {act_str}\nEXP: {exp_str}'

    @staticmethod
    def _get_actstr(actual_csvrow):
        csvfile = StringIO()
        wrcsv = writer(csvfile)
        wrcsv.writerow(actual_csvrow)
        return csvfile.getvalue().rstrip()


if __name__ == '__main__':
    test_stopat()
