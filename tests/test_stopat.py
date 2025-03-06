#!/usr/bin/env python3
"""Test `trk stop --at`"""

from os.path import exists
#from logging import basicConfig
#from logging import DEBUG
from logging import debug
from tempfile import TemporaryDirectory
from timetracker.utils import cyan
from timetracker.utils import yellow
from timetracker.cmd.init import run_init_test
from timetracker.cmd.start import run_start
#from timetracker.cmd.stop import run_stop
from tests.pkgtttest.dts import DT2525
from tests.pkgtttest.runfncs import RunBase
from tests.pkgtttest.runfncs import proj_setup

#basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'


def test_stopat(project='pumpkin', username='carver'):
    """Test `trk stop --at"""
    _run(Obj(project, username, dircur='dirproj', dirgit01=True))
    _run(Obj(project, username, dircur='dirdoc',  dirgit01=True))

def _run(obj):
    # Test researcher-entered datetime stoptimes
    obj.chk('4am',                   '2525-01-01 04:00:00')
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
        cfgp, _ = run_init_test(cfgname, dircsv, self.project, exp.dirhome, quiet=True)  # cfgg
        fin_start = run_start(cfgname, self.uname, now=DT2525, defaultdt=DT2525)
        assert exists(fin_start)
        assert stop_at, 'pylint'
        return 'pylint'
        #findhome(tmphome)


    def chk(self, stop_at, expstr):
        """Run stop --at and check value"""
        print(yellow(f'\nTEST: stop={stop_at:22} EXP={expstr}'))
        debug(cyan(f'\n{"="*100}'))
        debug(cyan(f'RUN(stop_at={stop_at})'))
        with TemporaryDirectory() as tmphome:
            stoptime = self._run(stop_at, tmphome)
            assert stoptime, 'pylint'
            #assert str(stoptime) == expstr, f'TEST({stop_at}): ACT({stoptime}) !=  EXP({expstr})'


if __name__ == '__main__':
    test_stopat()
