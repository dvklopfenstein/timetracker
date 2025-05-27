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
from timetracker.csvget import get_csvs_local_all
from timetracker.csvget import get_csvs_global_all
from tests.pkgtttest.runprojs import RunProjs
from tests.pkgtttest.mkprojs import get_projectname
from tests.pkgtttest.expcsvs import ExpCsvs


def test_cmd_projects(prt=True):
    """Test `trk stop --at"""
    userprojs = {
        ('david'  , 'shepherding'): ([('Sun', 'Fri', '5am', '11:30pm')], 111.0),
        ('david'  , 'sleeping'):    ([],   0.0),
        ('david'  , 'grazing'):     ([],   0.0),
        ('david'  , 'hunting'):     ([],   0.0),

        ('lambs'  , 'sleeping'):    ([('Mon', 'Sat',  '7pm',   '11pm')],  24.0),
        ('lambs'  , 'grazing'):     ([('Mon', 'Sat',  '6am',    '8am'),
                                      ('Mon', 'Sat',  '9am',   '10am'),
                                      ('Mon', 'Sat', '11am',   '12pm'),
                                      ('Mon', 'Sat',  '2am',    '3pm'),
                                      ('Mon', 'Sat', ' 7pm',    '8pm')], 108.0),
        ('goats'  , 'sleeping'):    ([('Mon', 'Sat',  '6:59pm', '11:59pm')], 30.0),  # 3
        ('goats'  , 'grazing'):     ([('Wed', 'Fri', '10am',    '4pm')],  18.0),

        ('lions'  , 'hunting'):     ([('Mon', 'Fri',  '7pm',    '8pm')],   5.0),
        ('lions'  , 'sleeping'):    ([],   0.0),
        ('lions'  , 'grazing'):     ([],   0.0),
        ('lions'  , 'shepherding'): ([],   0.0),
        ##('jackels', 'scavenging'):  ([('Sun', 'Fri',  '9am',    '3pm')],  36.0),
    }

    exp_projs = [
        'david/proj/shepherding/.timetracker/config',
        'david/proj/sleeping/.timetracker/config',
        'david/proj/grazing/.timetracker/config',
        'david/proj/hunting/.timetracker/config',

        'lambs/proj/sleeping/.timetracker/config',
        'lambs/proj/grazing/.timetracker/config',

        'goats/proj/sleeping/.timetracker/config',
        'goats/proj/grazing/.timetracker/config',

        'lions/proj/hunting/.timetracker/config',
        'lions/proj/sleeping/.timetracker/config',
        'lions/proj/grazing/.timetracker/config',
        'lions/proj/shepherding/.timetracker/config',
        ##'jackels/proj/scavenging/.timetracker/config',
    ]
    with TemporaryDirectory() as tmproot:
        # Initialize all projects for all usernames
        basicConfig()

        # Initialize all projects for all usernames
        runprojs = RunProjs(tmproot, userprojs)
        runprojs.run_setup()
        if prt:
            runprojs.prt_userfiles('FILES BEFORE PUSH/PULL', True)
        runprojs.chk_proj_configs(exp_projs)

        # Mimic git push and pull
        runprojs.all_push()
        pull_copies = runprojs.all_pull()
        if prt:
            runprojs.upstream.prt_files()
            runprojs.prt_userfiles('FILES AFTER PUSH/PULL', True)

        expobj = ExpCsvs(runprojs.orig_ntcsvs, pull_copies)
        # Find csvs for all users in all projects
        act_csvs = _test_get_csvs_global_all(runprojs.get_user2glbcfg(), runprojs.dirhome, prt)
        expobj.chk_get_csvs_global_all(act_csvs)

        # Find csvs for one user in all projects
        act_csvs = _test_get_csvs_global_uname(runprojs.get_user2glbcfg(), runprojs.dirhome, prt)
        expobj.chk_get_csvs_global_uname(act_csvs)

        # Find csvs for all users in one project
        act_csvs = _test_get_csvs_local_all(runprojs.prj2mgrprj, prt)
        expobj.chk_get_csvs_local_all(act_csvs)

        # Find csv for one user in one project
        act_csvs = _test_get_csv_local_uname(runprojs.prj2mgrprj, prt)
        expobj.chk_get_csvs_local_uname(act_csvs)

        #_test_run_hours_local_uname(runprojs.prj2mgrprj, runprojs.dirhome)
        #print(yellow('Print hours, iterating through all users & their projects'))
        #runprojs.run_hoursprojs()

        ##print(yellow('Print hours across projects globally'))
        ##print('FFFFFFFFFFFFFFFFFFFFFFFFFFFF', run_hours(runprojs.cfg, 'lambs', dirhome=tmproot))


#def _test_run_hours_local_uname(runprojs, runprojs.dirhome):


def _test_get_csvs_global_uname(user2glbcfg, dirhome, prt=False):
    """TEST get_csvs_global_uname(...)"""
    print(yellow('\nTEST get_csvs_global_uname(...)'))
    usr2ntcsvs = {}
    for usr, glb_cfg in user2glbcfg.items():
        projects = glb_cfg.get_projects()
        if prt:
            print(f'USERNAME: {usr}')
        # NtCsv: fcsv project username
        nts = get_csvs_global_uname(projects, usr, dirhome)
        usr2ntcsvs[usr] = set(nts)
        for ntcsv in nts:
            if prt:
                print(ntcsv)
            assert ntcsv.username == usr
        if prt:
            print('')
    return usr2ntcsvs

def _test_get_csvs_global_all(user2glbcfg, dirhome, prt=False):
    """TEST get_csvs_global_all(...)"""
    print(yellow('\nTEST get_csvs_global_all(...)'))
    usr2ntcsvs = {}
    for usr, glb_cfg in user2glbcfg.items():
        projects = glb_cfg.get_projects()
        if prt:
            print(f'USERNAME: {usr}')
        nts = get_csvs_global_all(projects, dirhome)
        usr2ntcsvs[usr] = set(nts)
        if prt:
            for ntcsv in nts:
                print(ntcsv)
            print('')
    return usr2ntcsvs

def _test_get_csv_local_uname(prj2mgrprj, prt=False):
    """TEST get_csv_local_uname(...)"""
    print(yellow('\nTEST get_csv_local_uname(...)'))
    usrprj2ntcsv = {}
    for (user, proj), obj in prj2mgrprj.items():
        ntd = get_csv_local_uname(obj.fcfgproj, user, obj.home)
        usrprj2ntcsv[(user, proj)] = ntd
        if ntd is not None:
            if prt:
                print(f'{user}: get_csv_local_uname({obj.fcfgproj}, {user}, {obj.home})')
                print(f'{ntd}\n')
            assert exists(ntd.fcsv)
            exp_fcsv = join(obj.fcfgproj.replace('.timetracker/config', ''),
                            f'timetracker_{ntd.project}_{user}.csv')
            assert ntd.username == user
            assert ntd.project == get_projectname(obj.fcfgproj)
            assert ntd.project == proj
            assert ntd.fcsv == exp_fcsv, f'fcsv: ACT != EXP\nACT({ntd.fcsv})\nEXP({exp_fcsv})'
    return usrprj2ntcsv

def _test_get_csvs_local_all(prj2mgrprj, prt=False):
    """TEST get_csv_local_uname(...)"""
    print(yellow('\nTEST get_csvs_local_all(...)'))
    usrprj2ntcsvs = {}
    for (user, proj), obj in prj2mgrprj.items():
        nts = get_csvs_local_all(obj.fcfgproj, obj.home)
        if nts is not None:
            usrprj2ntcsvs[(user, proj)] = set(nts)
            for ntd in nts:
                if prt:
                    print(f'{user:7} {proj} {ntd}')
            print('')
    return usrprj2ntcsvs


if __name__ == '__main__':
    test_cmd_projects()
