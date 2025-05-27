#!/usr/bin/env python3
"""Test `trk stop --at`"""

from os import system
from os.path import exists
from os.path import join
from io import StringIO
from logging import basicConfig
from logging import DEBUG
from logging import debug
from logging import getLogger
from tempfile import TemporaryDirectory
from csv import writer
from timetracker.consts import FILENAME_GLOBALCFG
from timetracker.utils import cyan
from timetracker.utils import yellow
from timetracker.ntcsv import get_ntcsv
from timetracker.cfg.cfg import Cfg
from timetracker.cfg.cfg_global import CfgGlobal
from timetracker.cmd.init import run_init
from timetracker.cmd.start import run_start
from timetracker.cmd.stop import run_stop
from tests.pkgtttest.dts import get_dt
from tests.pkgtttest.runfncs import RunBase
from tests.pkgtttest.runfncs import proj_setup

#basicConfig(level=DEBUG)
basicConfig()
getLogger("timetracker.epoch.epoch").setLevel(DEBUG)

SEP = f'\n{"="*80}\n'


def test_stopat(project='pumpkin', username='carver'):
    """Test `trk stop --at"""
    dta = get_dt(yearstr='2525', hour=8, minute=30)
    _run(dta, Obj(project, username, dircur='dirproj', dirgit01=True))
    _run(dta, Obj(project, username, dircur='dirdoc',  dirgit01=True))

def _run(dta, obj):
    # Test researcher-entered datetime stoptimes
    # pylint: disable=line-too-long
    obj.chk(dta, '11:30am',               '2525-01-01 08:30:00,3:00:00,,"A,B,C",')
    obj.chk(dta, "2525-02-19 17:00:00",   '2525-01-01 08:30:00,"49 days, 8:30:00",,"A,B,C",')
    obj.chk(dta, "2525-02-19 05:00:00 pm",'2525-01-01 08:30:00,"49 days, 8:30:00",,"A,B,C",')
    obj.chk(dta, "01-01 17:00:00",        '2525-01-01 08:30:00,8:30:00,,"A,B,C",')
    obj.chk(dta, "01-01 05:00:00 pm",     '2525-01-01 08:30:00,8:30:00,,"A,B,C",')
    # https://github.com/dateutil/dateutil/issues/1421 (5pm with a default datetime; 5pm w/no default works fine)
    obj.chk(dta, "01-1 5pm",      '2525-01-01 08:30:00,8:30:00,,"A,B,C",') # WORKS w/dataparser (not dateutil)
    obj.chk(dta, "01/01 5:00 pm", '2525-01-01 08:30:00,8:30:00,,"A,B,C",')
    obj.chk(dta, "1/1 5:30 pm",   '2525-01-01 08:30:00,9:00:00,,"A,B,C",')
    # Process researcher-entered stop-times containing two ':' as datetimes
    obj.chk(dta, "09:30:00",   '2525-01-01 08:30:00,1:00:00,,"A,B,C",')
    obj.chk(dta, "09:00:00",   '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
    obj.chk(dta, "4:00:00",    None)
    # Test researcher-entered datetime timedeltas
    obj.chk(dta, "30 minutes", '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
    obj.chk(dta, "30 min",     '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
    obj.chk(dta, "30min",      '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
    obj.chk(dta, "30:00",      '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
    obj.chk(dta, "4 hours",    '2525-01-01 08:30:00,4:00:00,,"A,B,C",')


class Obj(RunBase):
    """Test `trk stop --at`"""
    # pylint: disable=too-few-public-methods

    def _run(self, dta, stop_at, tmphome, dircsv=None):
        """Run init, stop --at, stop"""
        cfgname, finder, exp = proj_setup(tmphome, self.project, self.dircur, self.dirgit01)
        # pylint: disable=unused-variable
        fcfgg = join(exp.dirhome, FILENAME_GLOBALCFG)
        cfg = Cfg(cfgname, CfgGlobal(fcfgg))
        run_init(cfg, finder.dirgit, dircsv, self.project, dirhome=tmphome)
        ostart = run_start(cfg.cfg_loc, self.uname,
            now=dta,
            defaultdt=dta)
        assert exists(ostart.filename)
        csvfields = get_ntcsv("A,B,C", None, None)
        dct = run_stop(cfg.cfg_loc, self.uname, csvfields,
                       dirhome=tmphome,
                       stop_at=stop_at,
                       now=dta,
                       defaultdt=dta)
        assert dct is not None
        fcsv = dct['fcsv']
        assert fcsv == join(tmphome, 'proj/pumpkin/timetracker_pumpkin_carver.csv')
        if dct['csvline'] is not None:
            assert exists(fcsv)
        system(f'cat {fcsv}')
        #findhome(tmphome)
        return dct['csvline']

    def chk(self, start_at, stop_at, exp_csvstr):
        """Run stop --at and check value"""
        print(yellow(f'\nTEST: stop={stop_at:22} EXP={exp_csvstr}'))
        debug(cyan(f'\n{"="*100}'))
        debug(cyan(f'RUN(stop_at={stop_at})'))
        with TemporaryDirectory() as tmphome:
            act_list = self._run(start_at, stop_at, tmphome)
            print('ACTUAL LIST:', act_list)
            if act_list is not None:
                act_csvstr = self._get_actstr(act_list)
                assert act_csvstr == exp_csvstr, (
                    f'ERROR(stop_at: {stop_at})\n'
                    f'ACT({act_csvstr})\n'
                    f'EXP({exp_csvstr})')

    @staticmethod
    def _get_actstr(actual_csvrow):
        csvfile = StringIO()
        wrcsv = writer(csvfile, lineterminator="\n")
        wrcsv.writerow(actual_csvrow)
        return csvfile.getvalue().rstrip()


if __name__ == '__main__':
    test_stopat()
