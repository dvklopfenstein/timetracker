#!/usr/bin/env python3
"""Test `trk stop --at`"""

from os import environ
#from os import system
from os.path import join
#from io import StringIO
from logging import basicConfig
from logging import DEBUG
#from logging import debug
#from logging import getLogger
from tempfile import TemporaryDirectory
from collections import namedtuple
#from csv import writer
from timetracker.consts import FILENAME_GLOBALCFG
from timetracker.ntcsv import get_ntcsv
#from timetracker.utils import cyan
#from timetracker.utils import yellow
#from timetracker.ntcsv import get_ntcsv
from timetracker.cfg.cfg_global import CfgGlobal
from timetracker.cfg.cfg import Cfg
from timetracker.cmd.init import run_init
from timetracker.cmd.start import run_start_opcfg
from timetracker.cmd.stop import run_stop_opcfg
from timetracker.cmd.hours import run_hours
from timetracker.cmd.hours import cli_run_hours
#[from timetracker.cmd.hours import run_hours_global
#from timetracker.cmd.stop import run_stop
#from tests.pkgtttest.dts import get_dt
#from tests.pkgtttest.runfncs import RunBase
from tests.pkgtttest.runfncs import proj_setup
from tests.pkgtttest.mkprojs import findhome_str
from tests.pkgtttest.mkprojs import getmkdirs_filename
from tests.pkgtttest.mkprojs import reset_env
from tests.pkgtttest.dts import get_iter_weekday

# https://github.com/scrapinghub/dateparser/issues/1266
#from tests.pkgtttest.dts import DT2525
from tests.pkgtttest.dts import I1266 as DT2525

#getLogger("timetracker.epoch.epoch").setLevel(DEBUG)

SEP = f'\n{"="*80}\n'


def test_cmd_projects():
    """Test `trk stop --at"""
    userprojs = {
        ('david'  , 'shepharding'): [('Sun', 'Fri', '5am', '11:30pm')],
        ('lambs'  , 'grazing'):     [('Mon', 'Fri',  '6am',  '8am'),
                                     ('Mon', 'Fri',  '9am', '10am'),
                                     ('Mon', 'Fri', '11am', '12pm'),
                                     ('Mon', 'Fri',  '2am',  '3pm'),
                                     ('Mon', 'Fri', ' 7pm',  '8pm')],
        ('goats'  , 'grazing'):     [('Wed', 'Fri', '10am',  '4pm')],
        ('lions'  , 'hunting'):     [('Mon', 'Fri',  '7pm',  '8pm')],
        ('jackels', 'scavenging'):  [('Sun', 'Fri',  '9am',  '3pm')],
    }
    orig_fglb = environ.get('TIMETRACKERCONF')
    with TemporaryDirectory() as tmproot:
        # Initialize all projects for all usernames
        basicConfig()
        fglb = getmkdirs_filename(tmproot, 'share', FILENAME_GLOBALCFG)
        environ['TIMETRACKERCONF'] = fglb

        # `run_init` on each project
        mgr = RunAll(tmproot, userprojs, fglb)
        basicConfig(level=DEBUG)
        print(findhome_str(tmproot, '-type f'))

        # `run_start` and `run_stop` the specified times for each researcher & project
        for usrprj, times in userprojs.items():
            mgr.get_usrproj(usrprj).add_timeslots(times)
        print(findhome_str(tmproot, '-type f'))

        # Check projects listed in CfgGlobal
        mgr.chk_projects()

        # print hours, iterating through all users & their projects
        _run_init_projs(mgr, userprojs)

        # print hours across projects globally
        run_hours(mgr.cfg, 'lambs', dirhome=tmproot)

        # print hours across projects globally
        reset_env('TIMETRACKERCONF', orig_fglb, fglb)

def _run_init_projs(mgr, userprojs):
    """print hours, iterating through all users & their projects"""
    for usrprj, _ in userprojs.items():
        mgu = mgr.get_usrproj(usrprj)
        usr, _ = usrprj
        run_hours(mgr.cfg, usr, dirhome=mgu.home)
        cli_run_hours(mgr.cfg.cfg_loc.filename, mgu.get_args_hours())


class RunAll:
    """Manage all users and their projects"""

    def __init__(self, tmproot, userprojs, fcfg_global):
        self.dirhome = join(tmproot, 'home')
        self.userprojs = userprojs
        self.cfg_global = CfgGlobal(fcfg_global)
        self.cfg = Cfg("phoney.cfg", self.cfg_global)
        self.ups2mgr = {e:MngUsrProj(self.dirhome, self.cfg_global, *e) for e in userprojs}

    def get_usrproj(self, user_proj):
        """Get MngUsrProj for specified usernamd and project"""
        return self.ups2mgr.get(user_proj)

    def chk_projects(self):
        """Check the projects"""
        act_projs = self.cfg_global.get_projects()
        home = self.dirhome
        exp_projs = [
            ['shepharding', join(home, 'david/proj/shepharding/.timetracker/config')],
            ['grazing',     join(home, 'lambs/proj/grazing/.timetracker/config')],
            ['grazing',     join(home, 'goats/proj/grazing/.timetracker/config')],
            ['hunting',     join(home, 'lions/proj/hunting/.timetracker/config')],
            ['scavenging',  join(home, 'jackels/proj/scavenging/.timetracker/config')],
        ]
        assert act_projs == exp_projs, f'\nEXP:\n{exp_projs}\nACT:\n{act_projs}'


# pylint: disable=too-few-public-methods
class MngUsrProj:
    """Manage one user and the project"""

    # pylint: disable=unknown-option-value,too-many-arguments,too-many-positional-arguments
    def __init__(self, tmproot, cfg_global, user, projname, dircsv=None):
        self.cfg_global = cfg_global
        self.home = join(tmproot, user)
        self.user = user
        self.projname = projname
        print(f'\nMngUsrProj({self.home:29}, {user:7}, {projname})')
        self.fcfgproj, _, self.exp = proj_setup(self.home, projname, dircur='dirproj')
        self.cfg = run_init(self.fcfgproj,
            dircsv=dircsv,
            project=self.projname,
            dirhome=self.home,
            cfg_global=cfg_global)

    def get_args_hours(self):
        """Get cli args for run_hours"""
        nto = namedtuple('NtArgs', 'input name')
        return nto(input=self.cfg.cfg_loc.filename, name=self.user)

    def add_timeslots(self, timeslots):
        """Add time slots for every day between day0 and day1 for specified times"""
        for day0, day1, time0, time1 in timeslots:
            self._add_timeslots(day0, day1, time0, time1)

    def _add_timeslots(self, day0, day1, time0, time1):
        """Add time slots for every day between day0 and day1 for specified times"""
        cfg_loc = self.cfg.cfg_loc
        user = self.user
        for weekday in get_iter_weekday(day0, day1):
            start_at = f'{weekday} {time0}'
            stop_at  = f'{weekday} {time1}'
            msg = f'{start_at} -- {stop_at}'
            #print('ADDING TIMESLOT FOR', self.user, msg)
            run_start_opcfg(cfg_loc, user, start_at, defaultdt=DT2525, quiet=True)
            ntd = get_ntcsv(msg, activity=None, tags=None)
            run_stop_opcfg(cfg_loc, user, ntd, stop_at,  defaultdt=DT2525, quiet=True)
        #run_start_opcfg(self.cfg.cfg_loc, self.user, start_at=f'day

    ####dta = get_dt(yearstr='2525', hour=8, minute=30)
    ####_run(dta, Obj(project, username, dircur='dirproj', dirgit01=True))
    ####_run(dta, Obj(project, username, dircur='dirdoc',  dirgit01=True))

#def _run(dta, mgr):
#    # Test researcher-entered datetime stoptimes
#    # pylint: disable=line-too-long
#    mgr.chk(dta, '11:30am',               '2525-01-01 08:30:00,3:00:00,,"A,B,C",')
#    mgr.chk(dta, "2525-02-19 17:00:00",   '2525-01-01 08:30:00,"49 days, 8:30:00",,"A,B,C",')
#    mgr.chk(dta, "2525-02-19 05:00:00 pm",'2525-01-01 08:30:00,"49 days, 8:30:00",,"A,B,C",')
#    mgr.chk(dta, "01-01 17:00:00",        '2525-01-01 08:30:00,8:30:00,,"A,B,C",')
#    mgr.chk(dta, "01-01 05:00:00 pm",     '2525-01-01 08:30:00,8:30:00,,"A,B,C",')
#    # https://github.com/dateutil/dateutil/issues/1421 (5pm with a default datetime; 5pm w/no default works fine)
#    mgr.chk(dta, "01-1 5pm",      '2525-01-01 08:30:00,8:30:00,,"A,B,C",') # WORKS w/dataparser (not dateutil)
#    mgr.chk(dta, "01/01 5:00 pm", '2525-01-01 08:30:00,8:30:00,,"A,B,C",')
#    mgr.chk(dta, "1/1 5:30 pm",   '2525-01-01 08:30:00,9:00:00,,"A,B,C",')
#    # Process researcher-entered stop-times containing two ':' as datetimes
#    mgr.chk(dta, "09:30:00",   '2525-01-01 08:30:00,1:00:00,,"A,B,C",')
#    mgr.chk(dta, "09:00:00",   '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
#    mgr.chk(dta, "4:00:00",    None)
#    # Test researcher-entered datetime timedeltas
#    mgr.chk(dta, "30 minutes", '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
#    mgr.chk(dta, "30 min",     '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
#    mgr.chk(dta, "30min",      '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
#    mgr.chk(dta, "30:00",      '2525-01-01 08:30:00,0:30:00,,"A,B,C",')
#    mgr.chk(dta, "4 hours",    '2525-01-01 08:30:00,4:00:00,,"A,B,C",')
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
