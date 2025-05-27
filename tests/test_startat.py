#!/usr/bin/env python3
"""Test `trk start --at`"""

from os.path import exists
#from logging import basicConfig
#from logging import DEBUG
from logging import debug
from tempfile import TemporaryDirectory
from timetracker.utils import cyan
from timetracker.utils import yellow
from timetracker.cfg.cfg import Cfg
from timetracker.cmd.init import run_init
from timetracker.cmd.start import run_start
from tests.pkgtttest.dts import DT2525
from tests.pkgtttest.runfncs import RunBase
from tests.pkgtttest.runfncs import proj_setup

#basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'


def test_startat(project='pumpkin', username='carver'):
    """Test `trk start --at"""
    _run(Obj(project, username, dircur='dirproj', dirgit01=True))
    _run(Obj(project, username, dircur='dirdoc',  dirgit01=True))

def _run(obj):
    # pylint: disable=duplicate-code
    # Test researcher-entered datetime starttimes
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
    """Test `trk start --at`"""
    # pylint: disable=too-few-public-methods

    def _run(self, start_at, dircsv=None):
        """Run init, start --at, stop"""
        debug(cyan(f'\n{"="*100}'))
        debug(cyan(f'RUN(start_at={start_at})'))
        with TemporaryDirectory() as tmphome:
            cfgname, finder, _ = proj_setup(tmphome, self.project, self.dircur, self.dirgit01)

            # CMD: INIT; CFG PROJECT
            cfg = Cfg(cfgname)
            run_init(cfg, finder.dirgit, dircsv, self.project, dirhome=tmphome)
            #findhome(tmphome)

            # CMD: START
            ostart = run_start(cfg.cfg_loc, self.uname,
                                  start_at=start_at, now=DT2525, defaultdt=DT2525)
            assert exists(ostart.filename)
            return cfg.cfg_loc.get_starttime_obj(self.uname).read_starttime()


    def chk(self, start_at, expstr):
        """Run start --at and check value"""
        print(yellow(f'\nTEST: start={start_at:22} EXP={expstr}'))
        startdt = self._run(start_at)
        assert str(startdt) == expstr, f'TEST({start_at}): ACT({startdt}) !=  EXP({expstr})'


if __name__ == '__main__':
    test_startat()
