#!/usr/bin/env python3
"""Test the location of the csv file"""

from os.path import exists
from logging import basicConfig
from logging import DEBUG
from logging import debug
from tempfile import TemporaryDirectory
from timetracker.utils import cyan
from timetracker.cfg.finder import CfgFinder
from timetracker.cmd.init import run_init_test
from timetracker.cmd.start import run_start
from tests.pkgtttest.mkprojs import mk_projdirs
from tests.pkgtttest.mkprojs import findhome_str
from tests.pkgtttest.startdts import DT2525

basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'


def test_startat(project='pumpkin', username='carver'):
    """Test `trk start --at"""
    _run(Obj(project, username, dircur='dirproj', dirgit01=True))
    _run(Obj(project, username, dircur='dirdoc',  dirgit01=True))

def _run(obj):
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


class Obj:
    """Test the location of the csv file"""
    # pylint: disable=too-few-public-methods

    def __init__(self, project, username, dircur, dirgit01):
        self.project = project
        self.uname = username
        self.dircurattr = dircur
        self.dirgit01 = dirgit01

    def _run(self, start_at, dircsv=None):
        """Run init, start --at, stop"""
        debug(cyan(f'\n{"="*100}'))
        debug(cyan(f'RUN(start_at={start_at})'))
        with TemporaryDirectory() as tmphome:
            exp = mk_projdirs(tmphome, self.project, self.dirgit01)
            finder = CfgFinder(dircur=getattr(exp, self.dircurattr), trksubdir=None)
            cfgname = finder.get_cfgfilename()
            assert not exists(cfgname), findhome_str(exp.dirhome)

            # CMD: INIT; CFG PROJECT
            cfgp, _ = run_init_test(cfgname, dircsv, self.project, exp.dirhome)  # cfgg
            #findhome(tmphome)

            # CMD: START
            fin_start = run_start(cfgname, self.uname,
                                  start_at=start_at,
                                  now=DT2525,
                                  defaultdt=DT2525)
            assert exists(fin_start)
            return cfgp.get_starttime_obj(self.uname).read_starttime()


    def chk(self, start_at, expstr):
        """Run start --at and check value"""
        starttime = self._run(start_at)
        assert str(starttime) == expstr, f'TEST({start_at}): ACT({starttime}) !=  EXP({expstr})'


if __name__ == '__main__':
    test_startat()
