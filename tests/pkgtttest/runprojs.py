#!/usr/bin/env python3
"""Create and manage a set of user timetracker projects"""

from os.path import join
from os.path import dirname
from os.path import relpath
from logging import basicConfig
from logging import DEBUG
from collections import namedtuple
from timetracker.ntcsv import get_ntcsv
from timetracker.utils import yellow
from timetracker.cfg.doc_local import get_docproj
from timetracker.cfg.cfg_global import get_cfgglobal
from timetracker.cfg.docutils import get_value
from timetracker.cmd.init import run_init
from timetracker.cmd.start import run_start
from timetracker.cmd.stop import run_stop
from timetracker.cmd.hours import run_hours
from timetracker.cmd.hours import cli_run_hours
from tests.pkgtttest.consts import SEP1
from tests.pkgtttest.consts import SEP3
from tests.pkgtttest.runfncs import proj_setup
from tests.pkgtttest.userprojs import UserProjects
from tests.pkgtttest.upstream import Upstream
from tests.pkgtttest.mkprojs import get_type2files
from tests.pkgtttest.mkprojs import get_files
from tests.pkgtttest.mkprojs import prt_files
from tests.pkgtttest.dts import get_iter_weekday
from tests.pkgtttest.dts import td2hours
from tests.pkgtttest.dts import I1266 as DT2525


class RunProjs:
    """Manage all users and their projects"""

    def __init__(self, tmproot, userprojs):
        self.tmproot = tmproot
        self.dirhome = join(tmproot, 'home')
        self.ups = UserProjects(userprojs)
        self.prj2mgrprj = {(usr,prj):MngUsrProj(self.dirhome, usr, prj) for usr, prj in userprojs}
        self.upstream = Upstream(join(self.tmproot, 'upstream'))
        self.orig_ntcsvs = self.ups.get_expcsvs(self.tmproot)

    def all_push(self):
        """simulate a git-like push"""
        for (_, prj), obj in self.prj2mgrprj.items():
            dirproj = dirname(dirname(obj.cfg.cfg_loc.filename))
            files = get_files(dirproj)
            for absfname in files:
                relfname = relpath(absfname, dirproj)
                self.upstream.push(prj, absfname, relfname)

    def all_pull(self):
        """simulate a git-like pull"""
        pull_copies_all = []
        for (_, prj), obj in self.prj2mgrprj.items():
            dirproj = dirname(dirname(obj.cfg.cfg_loc.filename))
            pull_copies_cur = self.upstream.pull(prj, dirproj)
            pull_copies_all.extend(pull_copies_cur)
        return pull_copies_all

    def prt_userfiles(self, msg='FILES FOR ALL USERNAMES', prefix='USERFILE: '):
        """Print files for each username"""
        if prefix:
            prefix = f'{msg}: '
        print(f'\n{msg}:')
        for uname in self.ups.usernames:
            print(f'FILES FOR USERNAME: {uname}:')
            userhome = join(self.dirhome, uname)
            prt_files(userhome, prefix)

    def get_user2glbcfg(self):
        """For each username, get their one global config file"""
        user2glbcfg = {}
        for (usr, _), obj in self.prj2mgrprj.items():
            docproj = get_docproj(obj.fcfgproj)
            fcfg_doc = get_value(docproj, 'global_config', 'filename')
            cfg_glb = get_cfgglobal(dirhome=obj.home, fcfg_doc=fcfg_doc)
            assert cfg_glb is not None
            if usr not in user2glbcfg:
                user2glbcfg[usr] = cfg_glb
            else:
                assert cfg_glb.filename == user2glbcfg[usr].filename
        return user2glbcfg

    def run_setup(self):
        """Initialize and fill timeslots for multiple users and projects"""
        print(yellow(f"{SEP1}`run_init` on each project"))
        basicConfig(level=DEBUG)

        print(yellow('`run_start` and `run_stop` to fill each researcher & project'))
        self._run_start_stop_all()

        print(yellow('Check projects listed in CfgGlobal'))

    def _run_start_stop_all(self):
        """`run_start` and `run_stop` to fill each researcher & project"""
        for usrprj, (times, _) in self.ups.userprojs.items():
            mgrprj = self.prj2mgrprj[usrprj]
            mgrprj.add_timeslots(times)

    def chk_proj_configs(self, exp_fcfgprojs):
        """Check the projects"""
        type2files = get_type2files(self.tmproot)
        exp_fcfgprojs = set(join(self.dirhome, f) for f in exp_fcfgprojs)
        act_fcfgprojs = set(type2files['config'])
        assert set(act_fcfgprojs) == set(exp_fcfgprojs), self._errmsg(act_fcfgprojs, exp_fcfgprojs)

    def run_hoursprojs(self):
        """print hours, iterating through all users & their projects"""
        for usrprj, (_, exp_hours) in self.ups.userprojs.items():
            mgrprj = self.prj2mgrprj[usrprj]
            usr, _ = usrprj

            print(f'{SEP3}run_setup: run_hours project({usrprj[0]}) username({usrprj[1]})')
            # run_hours nt: RdCsvs: results errors ntcsvs
            run1 = run_hours(mgrprj.cfg, usr, dirhome=mgrprj.home)
            assert td2hours(run1.results) == self._get_total_hours(usr), (
                f'ACT({td2hours(run1.results)}) != EXP({self._get_total_hours(usr)}) '
                f'project({usrprj[0]}) username({usrprj[1]})')

            print(f'{SEP3}run_setup: cli_run_hours: project({usrprj[0]}) username({usrprj[1]})')
            # cli_run_hours nt: RdCsv:  results error
            run2 = cli_run_hours(mgrprj.cfg.cfg_loc.filename, mgrprj.get_args_hours())
            assert td2hours(run2.results) == exp_hours, \
                f'run_hours({run2.results}) != cli_run_hours({exp_hours}))'

    def _get_total_hours(self, usr):
        return sum(e for (u, _), (_, e) in self.ups.userprojs.items() if u == usr)

    @staticmethod
    def _errmsg(act_fcfgprojs, exp_fcfgprojs):
        txt = ['\nEXP:',]
        for fcfg in sorted(exp_fcfgprojs):
            txt.append(f'  {fcfg}')
        txt.append('\nACT:',)
        for fcfg in sorted(act_fcfgprojs):
            txt.append(f'  {fcfg}')
        return '\n'.join(txt)


# pylint: disable=too-few-public-methods
class MngUsrProj:
    """Manage one user and the project"""

    # pylint: disable=unknown-option-value,too-many-arguments,too-many-positional-arguments
    def __init__(self, tmproot, user, projname, dircsv=None):
        self.home = join(tmproot, user)
        self.user = user
        self.projname = projname
        self.cfg_global = get_cfgglobal(None, self.home, fcfg_doc=None)
        ##print(f'\nMngUsrProj({self.home:29}, {user:7}, {projname})')
        self.fcfgproj, _, self.exp = proj_setup(self.home, projname, dircur='dirproj')
        self.cfg = run_init(self.fcfgproj,
            dircsv=dircsv,
            project=self.projname,
            dirhome=self.home,
            cfg_global=self.cfg_global,
            quiet=True)

    def get_args_hours(self):
        """Get cli args for run_hours"""
        nto = namedtuple('NtArgs', 'fcsv name run_global global_config_file')
        #fcsv = self.cfg.cfg_loc.get_filename_csv(self.user, dirhome=self.home)
        #return nto(fcsv=fcsv, name=self.user)
        return nto(fcsv=None, name=self.user, run_global=False, global_config_file=None)

    def add_timeslots(self, timeslots):
        """Add time slots for every day between day0 and day1 for specified times"""
        for (day0, day1, time0, time1) in timeslots:
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
            run_start(cfg_loc, user, start_at, defaultdt=DT2525, quiet=True)
            ntd = get_ntcsv(msg, activity=None, tags=None)
            run_stop(cfg_loc, user, ntd, stop_at,  defaultdt=DT2525, quiet=True)
        #run_start(self.cfg.cfg_loc, self.user, start_at=f'day
