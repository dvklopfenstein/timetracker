#!/usr/bin/env python3
"""Test `trk stop --at`"""

from os import environ
from os.path import exists
from os.path import join
from logging import basicConfig
#from logging import DEBUG
from tempfile import TemporaryDirectory
from timetracker.consts import FILENAME_GLOBALCFG
from timetracker.utils import yellow
from timetracker.cmd.hours import run_hours
from timetracker.csvget import get_csv_local_uname
from timetracker.csvget import get_csvs_global_uname
from tests.pkgtttest.runprojs import RunProjs
from tests.pkgtttest.mkprojs import getmkdirs_filename
from tests.pkgtttest.mkprojs import reset_env
from tests.pkgtttest.mkprojs import get_projectname


def test_cmd_projects():
    """Test `trk stop --at"""
    userprojs = {
        ('david'  , 'shepherding'): ([('Sun', 'Fri', '5am', '11:30pm')], 111.0),
        ('lambs'  , 'sleeping'):    ([('Mon', 'Sat',  '7pm',   '11pm')],  24.0),
        ('lambs'  , 'grazing'):     ([('Mon', 'Sat',  '6am',    '8am'),
                                      ('Mon', 'Sat',  '9am',   '10am'),
                                      ('Mon', 'Sat', '11am',   '12pm'),
                                      ('Mon', 'Sat',  '2am',    '3pm'),
                                      ('Mon', 'Sat', ' 7pm',    '8pm')], 108.0),
        ('goats'  , 'sleeping'):    ([('Mon', 'Sat',  '6:59pm', '11:59pm')], 30.0),  # 3
        ('goats'  , 'grazing'):     ([('Wed', 'Fri', '10am',    '4pm')],  18.0),
        ('lions'  , 'hunting'):     ([('Mon', 'Fri',  '7pm',    '8pm')],   5.0),
        ('jackels', 'scavenging'):  ([('Sun', 'Fri',  '9am',    '3pm')],  36.0),
        # -------------------------------------------------------
        #('david'  , 'shepherding'): ([('Mon', 'Fri',  '5am',        '6am')],  5.0),  # 1
        #('lambs'  , 'grazing'):     ([('Mon', 'Fri',  '5am',        '7am')], 10.0),  # 2
        #('lambs'  , 'sleeping'):    ([('Mon', 'Fri',  '7pm',       '11pm')], 20.0),
        #('goats'  , 'grazing'):     ([('Mon', 'Fri',  '5am',        '8am')], 15.0),  # 3
        #('goats'  , 'sleeping'):    ([('Mon', 'Fri',  '6:59pm', '11:59pm')], 25.0),  # 3
        #('lions'  , 'hunting'):     ([('Mon', 'Fri',  '5am',        '9am')], 20.0),  # 4
        #('jackels', 'scavenging'):  ([('Mon', 'Fri',  '5am',       '10am')], 25.0),  # 5
    }
    exp_projs = [
        ['shepherding', 'david/proj/shepherding/.timetracker/config'],
        ['sleeping',    'lambs/proj/sleeping/.timetracker/config'],
        ['grazing',     'lambs/proj/grazing/.timetracker/config'],
        ['sleeping',    'goats/proj/sleeping/.timetracker/config'],
        ['grazing',     'goats/proj/grazing/.timetracker/config'],
        ['hunting',     'lions/proj/hunting/.timetracker/config'],
        ['scavenging',  'jackels/proj/scavenging/.timetracker/config'],
    ]
    orig_fglb = environ.get('TIMETRACKERCONF')
    with TemporaryDirectory() as tmproot:
        # Initialize all projects for all usernames
        basicConfig()
        fglb = getmkdirs_filename(tmproot, 'share', FILENAME_GLOBALCFG)
        environ['TIMETRACKERCONF'] = fglb

        runall = RunProjs(tmproot, fglb, userprojs)
        runall.run_setup(exp_projs)

        #type2files = get_type2files(runall.dirhome)
        _prt_projs(runall.prj2mgrprj, runall.dirhome)

        _test_get_csv_local_uname(runall.prj2mgrprj, runall.dirhome)
        _test_get_csvs_global_uname(runall.get_user2glbcfg(), runall.dirhome)

        #_test_run_hours_local_uname(runall.prj2mgrprj, runall.dirhome)
        #print(yellow('Print hours, iterating through all users & their projects'))
        #runall.run_hoursprojs()

        print(yellow('Print hours across projects globally'))
        print('FFFFFFFFFFFFFFFFFFFFFFFFFFFF', run_hours(runall.cfg, 'lambs', dirhome=tmproot))

        #print(yellow('Print hours across projects globally'))
        reset_env('TIMETRACKERCONF', orig_fglb, fglb)

#def _test_run_hours_local_uname(runall, runall.dirhome):


def _prt_projs(prj2mgrprj, dirhome):
    for (user, proj), obj in prj2mgrprj.items():
        print(f'{dirhome} {user:7} {proj:11} {obj.fcfgproj}')


def _test_get_csvs_global_uname(user2glbcfg, dirhome):
    """TEST get_csvs_global_uname(...)"""
    print(yellow('\nTEST get_csvs_global_uname(...)'))
    for usr, glb_cfg in user2glbcfg.items():
        print(f'USERNAME: {usr}')
        projects = glb_cfg.get_projects()
        nts = get_csvs_global_uname(projects, usr, dirhome)
        for ntd in nts:
            exp_fcsv = join(ntd.fcfgproj.replace('.timetracker/config', ''),
                            f'timetracker_{ntd.ntcsv.project}_{usr}.csv')
            print(ntd)
            assert ntd.ntcsv.username == usr
            assert ntd.ntcsv.project == get_projectname(ntd.fcfgproj)
            assert ntd.ntcsv.fcsv == exp_fcsv
            #assert ntd.project == get_projectname(obj.fcfgproj)
        ##assert projects == [nt.fcfgproj for nt in nts], (f'ACT != EXP\n'
        ##                                                 f'ACT: {projects}\n'
        ##                                                 f'EXP: {[nt.fcfgproj for nt in nts]}\n')
        print('')

def _test_get_csv_local_uname(prj2mgrprj, dirhome):
    """TEST get_csv_local_uname(...)"""
    print(yellow('\nTEST get_csv_local_uname(...)'))
    for (user, proj), obj in prj2mgrprj.items():
        ntd = get_csv_local_uname(obj.fcfgproj, user, dirhome)
        ##print(f'TEST get_csv_local_uname({obj.fcfgproj}, {user}, {dirhome})')
        ##print(f'{ntd}\n')
        assert exists(ntd.fcsv)
        exp_fcsv = join(obj.fcfgproj.replace('.timetracker/config', ''),
                        f'timetracker_{ntd.project}_{user}.csv')
        assert ntd.username == user
        assert ntd.project == get_projectname(obj.fcfgproj)
        assert ntd.project == proj
        assert ntd.fcsv == exp_fcsv, f'fcsv: ACT != EXP\nACT({ntd.fcsv})\nEXP({exp_fcsv})'


if __name__ == '__main__':
    test_cmd_projects()
