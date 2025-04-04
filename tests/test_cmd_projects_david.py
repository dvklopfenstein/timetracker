#!/usr/bin/env python3
"""Test `trk stop --at`"""

#from os import system
#from os.path import exists
from os.path import join
from os.path import dirname
#from io import StringIO
from logging import basicConfig
from logging import DEBUG
#from logging import debug
#from logging import getLogger
from tempfile import TemporaryDirectory
#from csv import writer
#from timetracker.consts import FILENAME_GLOBALCFG
#from timetracker.utils import cyan
#from timetracker.utils import yellow
#from timetracker.ntcsv import get_ntcsv
from timetracker.cmd.init import run_init
#from timetracker.cmd.start import run_start
#from timetracker.cmd.stop import run_stop
#from tests.pkgtttest.dts import get_dt
from tests.pkgtttest.runfncs import findhome_str
#from tests.pkgtttest.runfncs import RunBase
from tests.pkgtttest.runfncs import proj_setup

#getLogger("timetracker.epoch.epoch").setLevel(DEBUG)

SEP = f'\n{"="*80}\n'


def test_cmd_projects():
    """Test `trk stop --at"""
    userprojs = [
        ('david'  , 'shepharding'),
        ('lambs'  , 'grazing'),
        ('goats'  , 'grazing'),
        ('lions'  , 'hunting'),
        ('jackels', 'scavenging'),
    ]
    with TemporaryDirectory() as tmproot:
        basicConfig()
        obj = RunAll(tmproot, userprojs)
        basicConfig(level=DEBUG)
        print(findhome_str(tmproot))
        assert obj


# pylint: disable=too-few-public-methods
class RunAll:
    """Manage all users and their projects"""

    def __init__(self, tmproot, userprojs):
        self.dirhome = join(tmproot, 'home')
        self.cfg1 = join(tmproot, 'dflt.cfg')
        self.userprojs = userprojs
        self.ups2obj = {e:RunOne(self.cfg1, *e) for e in userprojs}

class RunOne:
    """Manage one user and the project"""

    def __init__(self, fcfgdflt, user, projname):
        self.cfg_global = fcfgdflt
        self.home = join(dirname(self.cfg_global), user)
        self.user = user
        self.projname = projname
        print(f'\nRunOne({self.home:29}, {user:7}, {projname})')
        self.fcfgproj, _, self.exp = proj_setup(self.home, projname, dircur='dirproj')
        self.cfg = run_init(self.fcfgproj,
            dircsv=None,
            project=self.projname,
            dirhome=self.home,
            fcfg_global=fcfgdflt)

    ####dta = get_dt(yearstr='2525', hour=8, minute=30)
    ####_run(dta, Obj(project, username, dircur='dirproj', dirgit01=True))
    ####_run(dta, Obj(project, username, dircur='dirdoc',  dirgit01=True))

#def _run(dta, obj):
#    # Test researcher-entered datetime stoptimes
#    # pylint: disable=line-too-long
#    obj.chk(dta, '11:30am',               '2525-01-01 08:30:00,3:00:00,,"A,B,C",')
#    obj.chk(dta, "2525-02-19 17:00:00",   '2525-01-01 08:30:00,"49 days, 8:30:00",,"A,B,C",')
#    obj.chk(dta, "2525-02-19 05:00:00 pm",'2525-01-01 08:30:00,"49 days, 8:30:00",,"A,B,C",')
#    obj.chk(dta, "01-01 17:00:00",        '2525-01-01 08:30:00,8:30:00,,"A,B,C",')
#    obj.chk(dta, "01-01 05:00:00 pm",     '2525-01-01 08:30:00,8:30:00,,"A,B,C",')
#    # https://github.com/dateutil/dateutil/issues/1421 (5pm with a default datetime; 5pm w/no default works fine)
#    obj.chk(dta, "01-1 5pm",      '2525-01-01 08:30:00,8:30:00,,"A,B,C",') # WORKS w/dataparser (not dateutil)
#    obj.chk(dta, "01/01 5:00 pm", '2525-01-01 08:30:00,8:30:00,,"A,B,C",')
#    obj.chk(dta, "1/1 5:30 pm",   '2525-01-01 08:30:00,9:00:00,,"A,B,C",')
#    # Process researcher-entered stop-times containing two ':' as datetimes
#    obj.chk(dta, "09:30:00",   '2525-01-01 08:30:00,1:00:00,,"A,B,C",')
#    obj.chk(dta, "09:00:00",   '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
#    obj.chk(dta, "4:00:00",    None)
#    # Test researcher-entered datetime timedeltas
#    obj.chk(dta, "30 minutes", '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
#    obj.chk(dta, "30 min",     '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
#    obj.chk(dta, "30min",      '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
#    obj.chk(dta, "30:00",      '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
#    obj.chk(dta, "4 hours",    '2525-01-01 08:30:00,4:00:00,,"A,B,C",')
#
#
#class Obj(RunBase):
#    """Test `trk stop --at`"""
#    # pylint: disable=too-few-public-methods
#
#    def _run(self, dta, stop_at, tmphome, dircsv=None):
#        """Run init, stop --at, stop"""
#        cfgname, _, exp = proj_setup(tmphome, self.project, self.dircur, self.dirgit01)
#        # pylint: disable=unused-variable
#        fcfgg = join(exp.dirhome, FILENAME_GLOBALCFG)
#        run_init(cfgname, dircsv, self.project, dirhome=tmphome)
#        fin_start = run_start(cfgname, self.uname,
#            now=dta,
#            defaultdt=dta)
#        assert exists(fin_start)
#        csvfields = get_ntcsv("A,B,C", None, None)
#        dct = run_stop(cfgname, self.uname, csvfields,
#                       dirhome=tmphome,
#                       stop_at=stop_at,
#                       now=dta,
#                       defaultdt=dta)
#        assert dct is not None
#        fcsv = dct['fcsv']
#        assert fcsv == join(tmphome, 'proj/pumpkin/timetracker_pumpkin_carver.csv')
#        if dct['csvline'] is not None:
#            assert exists(fcsv)
#        system(f'cat {fcsv}')
#        #findhome(tmphome)
#        return dct['csvline']
#
#    def chk(self, start_at, stop_at, exp_csvstr):
#        """Run stop --at and check value"""
#        print(yellow(f'\nTEST: stop={stop_at:22} EXP={exp_csvstr}'))
#        debug(cyan(f'\n{"="*100}'))
#        debug(cyan(f'RUN(stop_at={stop_at})'))
#        with TemporaryDirectory() as tmphome:
#            act_list = self._run(start_at, stop_at, tmphome)
#            print('ACTUAL LIST:', act_list)
#            if act_list is not None:
#                act_csvstr = self._get_actstr(act_list)
#                assert act_csvstr == exp_csvstr, (
#                    f'ERROR(stop_at: {stop_at})\n'
#                    f'ACT({act_csvstr})\n'
#                    f'EXP({exp_csvstr})')
#
#    @staticmethod
#    def _get_actstr(actual_csvrow):
#        csvfile = StringIO()
#        wrcsv = writer(csvfile, lineterminator="\n")
#        wrcsv.writerow(actual_csvrow)
#        return csvfile.getvalue().rstrip()


if __name__ == '__main__':
    test_cmd_projects()
