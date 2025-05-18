#!/usr/bin/env python3
"""Test `trk stop --at`"""

from os.path import exists
from os.path import join
from logging import basicConfig
from tempfile import TemporaryDirectory
from timetracker.utils import yellow
#from timetracker.cmd.hours import run_hours
from timetracker.csvget import get_csv_local_uname
from timetracker.csvget import get_csvs_global_uname
from tests.pkgtttest.runprojs import RunProjs
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
    }

    exp_projs = [
        'david/proj/shepherding/.timetracker/config',
        'lambs/proj/sleeping/.timetracker/config',
        'lambs/proj/grazing/.timetracker/config',
        'goats/proj/sleeping/.timetracker/config',
        'goats/proj/grazing/.timetracker/config',
        'lions/proj/hunting/.timetracker/config',
        'jackels/proj/scavenging/.timetracker/config',
    ]
    with TemporaryDirectory() as tmproot:
        # Initialize all projects for all usernames
        basicConfig()

        runprojs = RunProjs(tmproot, userprojs)
        runprojs.run_setup()
        runprojs.prt_userfiles()
        runprojs.chk_proj_configs(exp_projs)

        prt = True
        _test_get_csv_local_uname(runprojs.prj2mgrprj, prt)
        _test_get_csvs_global_uname(runprojs.get_user2glbcfg(), runprojs.dirhome, prt)

        #_test_run_hours_local_uname(runprojs.prj2mgrprj, runprojs.dirhome)
        #print(yellow('Print hours, iterating through all users & their projects'))
        #runprojs.run_hoursprojs()

        print(yellow('Print hours across projects globally'))
        ##print('FFFFFFFFFFFFFFFFFFFFFFFFFFFF', run_hours(runprojs.cfg, 'lambs', dirhome=tmproot))


#def _test_run_hours_local_uname(runprojs, runprojs.dirhome):


def _test_get_csvs_global_uname(user2glbcfg, dirhome, prt=False):
    """TEST get_csvs_global_uname(...)"""
    print(yellow('\nTEST get_csvs_global_uname(...)'))
    for usr, glb_cfg in user2glbcfg.items():
        projects = glb_cfg.get_projects()
        if prt:
            print(f'USERNAME: {usr}')
        nts = get_csvs_global_uname(projects, usr, dirhome)
        for ntd in nts:
            exp_fcsv = join(ntd.fcfgproj.replace('.timetracker/config', ''),
                            f'timetracker_{ntd.ntcsv.project}_{usr}.csv')
            if prt:
                print(ntd)
            assert ntd.ntcsv.username == usr
            assert ntd.ntcsv.project == get_projectname(ntd.fcfgproj)
            assert ntd.ntcsv.fcsv == exp_fcsv
            #assert ntd.project == get_projectname(obj.fcfgproj)
        ##assert projects == [nt.fcfgproj for nt in nts], (f'ACT != EXP\n'
        ##                                                 f'ACT: {projects}\n'
        ##                                                 f'EXP: {[nt.fcfgproj for nt in nts]}\n')
        print('')

def _test_get_csv_local_uname(prj2mgrprj, prt=False):
    """TEST get_csv_local_uname(...)"""
    print(yellow('\nTEST get_csv_local_uname(...)'))
    for (user, proj), obj in prj2mgrprj.items():
        ntd = get_csv_local_uname(obj.fcfgproj, user, obj.home)
        if prt:
            print(f'TEST {user}: get_csv_local_uname({obj.fcfgproj}, {user}, {obj.home})')
            print(f'{ntd}\n')
        assert exists(ntd.fcsv)
        exp_fcsv = join(obj.fcfgproj.replace('.timetracker/config', ''),
                        f'timetracker_{ntd.project}_{user}.csv')
        assert ntd.username == user
        assert ntd.project == get_projectname(obj.fcfgproj)
        assert ntd.project == proj
        assert ntd.fcsv == exp_fcsv, f'fcsv: ACT != EXP\nACT({ntd.fcsv})\nEXP({exp_fcsv})'


if __name__ == '__main__':
    test_cmd_projects()
