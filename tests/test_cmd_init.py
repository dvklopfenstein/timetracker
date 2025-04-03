#!/usr/bin/env python3
"""Test the TimeTracker init command.

Headers:
    G: Global timetracker file           ~/.timetrackerconfig
    g: Git repo dir                      ./.git/
    L: Local  timetracker file           ./.timetracker/config
    S: timetracker file start time file  ./.timetracker/start_PROJ_USER.txt

Values:
    0: file or directory does not exist
    1: file or directory does exists

GgLS X Description
---- - -----------------------------------
0000 . fatal: not a trk repository (or any of the parent directories): ./.timetracker
0001 X
0010 X
0011
0100
0101
0110
0111
1000
1001
1010
1011
1100
1101
1110
1111

TIMETRACKER ARGS: Namespace(
 trk_dir='.ttt',
 name='dvklo',
 command='init',
 dircsv='/home/dvklo/timetrackers',
 project='timetracker',
 force=False,
 global_config_file='/home/dvklo/timetrackers/config')

"""

# from os import makedirs
from os.path import exists
from os.path import join
from collections import namedtuple
from logging import basicConfig
from logging import DEBUG
#from logging import debug
from tempfile import TemporaryDirectory

from timetracker.cmd.init import run_init

from tests.pkgtttest.runfncs import proj_setup
#from timetracker.cmd.init import run_reinit
# from tempfile import TemporaryDirectory
# from timetracker.cfg.finder import CfgFinder
# from tests.pkgtttest.mkprojs import mkdirs
# from tests.pkgtttest.mkprojs import findhome


basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'
NTO = namedtuple('Args', 'trk_dir name dircsv project force global_config_file')

def test_cmd_init(project='apple', user='picker'):
    """Test the TimeTracker init command"""
    _run_0(project, user)
    _run_proj(project, user)
    _run_csv(project, user)
    _run_gcfg(project, user)

# ================================================================================
def _run_0(project, user):
    with TemporaryDirectory() as tmphome:
        fcfgproj, _, ntdirs = proj_setup(tmphome, project, dircur='dirproj', dirgit01=True)
        cfg_top = run_init(fcfgproj, dirhome=tmphome)  # , project, force, global_config_file)

        _chk_cfg_loc(cfg_top.cfg_loc, project, user,
            exp_cfg_filename=ntdirs.cfglocfilename,
            exp_cfg_csv_filename='./timetracker_PROJECT_$USER$.csv',
            exp_filename_csv=join(ntdirs.dirproj, 'timetracker_apple_picker.csv'))
        _chk_cfg_global(cfg_top.cfg_glb, project,
            exp_glb_filename=join(ntdirs.dirhome, '.timetrackerconfig'),
            exp_loc_filename=ntdirs.cfglocfilename)

# ================================================================================
def _run_proj(project, user):
    with TemporaryDirectory() as tmphome:
        newproj = 'pear'
        fcfgproj, _, ntdirs = proj_setup(tmphome, project, dircur='dirproj', dirgit01=True)
        cfg_top = run_init(fcfgproj, dirhome=tmphome, project=newproj)  #force, global_config_file)

        _chk_cfg_loc(cfg_top.cfg_loc, newproj, user,
            exp_cfg_filename=ntdirs.cfglocfilename,
            exp_cfg_csv_filename='./timetracker_PROJECT_$USER$.csv',
            exp_filename_csv=join(ntdirs.dirproj, 'timetracker_pear_picker.csv'))
        _chk_cfg_global(cfg_top.cfg_glb, newproj,
            exp_glb_filename=join(ntdirs.dirhome, '.timetrackerconfig'),
            exp_loc_filename=ntdirs.cfglocfilename)

# ================================================================================
def _run_csv(project, user):
    with TemporaryDirectory() as tmphome:
        newproj = 'pear'
        fcfgproj, _, ntdirs = proj_setup(tmphome, project, dircur='dirproj', dirgit01=True)
        cfg_top = run_init(fcfgproj, dirhome=tmphome, dircsv=tmphome, project=newproj)

        _chk_cfg_loc(cfg_top.cfg_loc, newproj, user,
            exp_cfg_filename=ntdirs.cfglocfilename,
            exp_cfg_csv_filename=join(tmphome, 'timetracker_PROJECT_$USER$.csv'),
            exp_filename_csv=join(tmphome, 'timetracker_pear_picker.csv'))
        _chk_cfg_global(cfg_top.cfg_glb, newproj,
            exp_glb_filename=join(ntdirs.dirhome, '.timetrackerconfig'),
            exp_loc_filename=ntdirs.cfglocfilename)

# ================================================================================
def _run_gcfg(project, user):
    with TemporaryDirectory() as tmphome:
        newproj = 'pear'
        newgcfg = join(tmphome, 'myglobal.cfg')
        fcfgproj, _, ntdirs = proj_setup(tmphome, project, dircur='dirproj', dirgit01=True)
        cfg_top = run_init(fcfgproj, dirhome=tmphome, dircsv=tmphome, project=newproj,
            fcfg_global=newgcfg)

        doc_loc = _chk_cfg_loc(cfg_top.cfg_loc, newproj, user,
            exp_cfg_filename=ntdirs.cfglocfilename,
            exp_cfg_csv_filename=join(tmphome, 'timetracker_PROJECT_$USER$.csv'),
            exp_filename_csv=join(tmphome, 'timetracker_pear_picker.csv'))
        # pylint: disable=unsubscriptable-object
        assert doc_loc['global_config']['filename'] == cfg_top.cfg_glb.filename
        _chk_cfg_global(cfg_top.cfg_glb, newproj,
            exp_glb_filename=newgcfg,
            exp_loc_filename=ntdirs.cfglocfilename)

# --------------------------------------------------------------------------------
def _chk_cfg_global(cfg_glb, project, exp_glb_filename, exp_loc_filename):
    assert cfg_glb.filename == exp_glb_filename, \
        f'EXP({exp_glb_filename}) != ACT({cfg_glb.filename})'
    assert exists(cfg_glb.filename), f'SHOULD EXIST: {cfg_glb.filename}'
    doc_glb = cfg_glb.read_doc()
    assert doc_glb['projects'] == [
        [project, exp_loc_filename],
    ]
    print(doc_glb)

# pylint: disable=unknown-option-value
# pylint: disable=too-many-arguments,too-many-positional-arguemnts
def _chk_cfg_loc(cfg_loc, project, user, exp_cfg_filename, exp_cfg_csv_filename, exp_filename_csv):
    # Check CfgProj values
    assert cfg_loc.filename == exp_cfg_filename
    assert exists(cfg_loc.filename), f'CFG NOT EXIST({cfg_loc.filename})'
    doc_loc = cfg_loc.read_doc()
    print(doc_loc)
    assert doc_loc['project'] == project
    assert doc_loc['csv']['filename'] == exp_cfg_csv_filename, \
        f"ACT({doc_loc['csv']['filename']}) != EXP({exp_cfg_csv_filename})"
    act_csv = cfg_loc.get_filename_csv(user)
    print(act_csv)
    assert act_csv == exp_filename_csv
    return doc_loc


if __name__ == '__main__':
    test_cmd_init()
