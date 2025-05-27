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
from logging import basicConfig
from logging import DEBUG
#from logging import debug
from tempfile import TemporaryDirectory
from pytest import raises

from timetracker.utils import yellow
from timetracker.cfg.cfg import Cfg
from timetracker.cfg.doc_local import DocProj
from timetracker.cmd.init import run_init
from timetracker.cfg.tomutils import read_config

from tests.pkgtttest.cmpstr import str_file
from tests.pkgtttest.runfncs import proj_setup
#from timetracker.cmd.init import run_reinit
# from tempfile import TemporaryDirectory
# from timetracker.cfg.finder import CfgFinder
# from tests.pkgtttest.mkprojs import mkdirs
# from tests.pkgtttest.mkprojs import findhome


basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'

def test_cmd_init(project='apple', user='picker'):
    """Test the TimeTracker init command"""
    _run_0(project, user)
    _run_proj(   project, user, 'pear')
    _run_csv(    project, user, 'pear')
    _run_gcfg(   project, user, 'pear', 'a.cfg')
    _run_gcfg_ab(project, user, 'pear', 'a.cfg', 'b.cfg')

# ================================================================================
def _run_0(project, user):
    print(yellow(f'{SEP}NO PROJECT GIVEN'))
    with TemporaryDirectory() as tmphome:
        fcfgproj, finder, ntdirs = proj_setup(tmphome, project, dircur='dirproj', dirgit01=True)
        cfg_top = Cfg(fcfgproj)
        run_init(cfg_top, finder.dirgit, dirhome=tmphome)

        _chk_cfg_loc(cfg_top.cfg_loc, project, user,
            exp_cfg_filename=ntdirs.cfglocfilename,
            exp_cfg_csv_filename=f'./timetracker_{project}_$USER$.csv',
            exp_filename_csv=join(ntdirs.dirproj, 'timetracker_apple_picker.csv'))
        _chk_cfg_global(cfg_top.cfg_glb, project,
            exp_glb_filename=join(ntdirs.dirhome, '.timetrackerconfig'),
            exp_loc_filename=ntdirs.cfglocfilename)

# ================================================================================
def _run_proj(project, user, newproj):
    print(yellow(f'{SEP}'), end='')
    with TemporaryDirectory() as tmphome:
        fcfgproj, finder, ntdirs = proj_setup(tmphome, project, dircur='dirproj', dirgit01=True)
        cfg_top = Cfg(fcfgproj)
        run_init(cfg_top, finder.dirgit, dirhome=tmphome,
            project=newproj)  #force, global_config_file)

        _chk_cfg_loc(cfg_top.cfg_loc, newproj, user,
            exp_cfg_filename=ntdirs.cfglocfilename,
            exp_cfg_csv_filename=f'./timetracker_{newproj}_$USER$.csv',
            exp_filename_csv=join(ntdirs.dirproj, f'timetracker_{newproj}_picker.csv'))
        _chk_cfg_global(cfg_top.cfg_glb, newproj,
            exp_glb_filename=join(ntdirs.dirhome, '.timetrackerconfig'),
            exp_loc_filename=ntdirs.cfglocfilename)

# ================================================================================
def _run_csv(project, user, newproj):
    print(yellow(f'{SEP}'), end='')
    with TemporaryDirectory() as tmphome:
        fcfgproj, finder, ntdirs = proj_setup(tmphome, project, dircur='dirproj', dirgit01=True)
        cfg_top = Cfg(fcfgproj)
        run_init(cfg_top, finder.dirgit, dirhome=tmphome,
            project=newproj,
            dircsv=tmphome)

        _chk_cfg_loc(cfg_top.cfg_loc, newproj, user,
            exp_cfg_filename=ntdirs.cfglocfilename,
            exp_cfg_csv_filename=join(tmphome, f'timetracker_{newproj}_$USER$.csv'),
            exp_filename_csv=join(tmphome, 'timetracker_pear_picker.csv'))
        _chk_cfg_global(cfg_top.cfg_glb, newproj,
            exp_glb_filename=join(ntdirs.dirhome, '.timetrackerconfig'),
            exp_loc_filename=ntdirs.cfglocfilename)

# ================================================================================
def _run_gcfg(project, user, newproj, fcfg_glb):
    print(yellow(f'{SEP}'), end='')
    with TemporaryDirectory() as tmphome:
        newgcfg = join(tmphome, fcfg_glb)
        fcfgproj, finder, ntdirs = proj_setup(tmphome, project, dircur='dirproj', dirgit01=True)
        cfg_top = Cfg(fcfgproj)
        run_init(cfg_top, finder.dirgit, dirhome=tmphome,
            project=newproj,
            dircsv=tmphome,
            fcfg_global=newgcfg)

        doc_loc = _chk_cfg_loc(cfg_top.cfg_loc, newproj, user,
            exp_cfg_filename=ntdirs.cfglocfilename,
            exp_cfg_csv_filename=join(tmphome, f'timetracker_{newproj}_$USER$.csv'),
            exp_filename_csv=join(tmphome, 'timetracker_pear_picker.csv'))
        # pylint: disable=unsubscriptable-object
        assert doc_loc.global_config_filename == cfg_top.cfg_glb.filename
        _chk_cfg_global(cfg_top.cfg_glb, newproj,
            exp_glb_filename=newgcfg,
            exp_loc_filename=ntdirs.cfglocfilename)

# ================================================================================
def _run_gcfg_ab(project, user, newproj, fcfg_glba, fcfg_glbb):
    print(yellow(f'{SEP}'), end='')
    with TemporaryDirectory() as tmphome:
        newgcfg_a = join(tmphome, fcfg_glba)
        newgcfg_b = join(tmphome, fcfg_glbb)
        fcfgproj, finder, ntdirs = proj_setup(tmphome, project, dircur='dirproj', dirgit01=True)
        cfg_top = Cfg(fcfgproj)
        run_init(cfg_top, finder.dirgit, dirhome=tmphome,
            project=newproj,
            dircsv=tmphome,
            fcfg_global=newgcfg_a)

        doc_loc = _chk_cfg_loc(cfg_top.cfg_loc, newproj, user,
            exp_cfg_filename=ntdirs.cfglocfilename,
            exp_cfg_csv_filename=join(tmphome, f'timetracker_{newproj}_$USER$.csv'),
            exp_filename_csv=join(tmphome, 'timetracker_pear_picker.csv'))
        # pylint: disable=unsubscriptable-object
        assert doc_loc.global_config_filename == cfg_top.cfg_glb.filename
        _chk_cfg_global(cfg_top.cfg_glb, newproj,
            exp_glb_filename=newgcfg_a,
            exp_loc_filename=ntdirs.cfglocfilename)

        with raises(SystemExit) as excinfo:
            run_init(cfg_top, finder.dirgit, dirhome=tmphome,
                project=newproj,
                dircsv=tmphome,
                fcfg_global=newgcfg_b)
            assert excinfo.value.code == 0

# --------------------------------------------------------------------------------
def _chk_cfg_global(cfg_glb, project, exp_glb_filename, exp_loc_filename):
    assert cfg_glb.filename == exp_glb_filename, \
        f'EXP({exp_glb_filename}) != ACT({cfg_glb.filename})'
    assert exists(cfg_glb.filename), f'SHOULD EXIST: {cfg_glb.filename}'
    projects = cfg_glb.get_projects()
    assert projects == [
        [project, exp_loc_filename],
    ]

# pylint: disable=unknown-option-value
# pylint: disable=too-many-arguments,too-many-positional-arguments
def _chk_cfg_loc(cfg_loc, project, user, exp_cfg_filename, exp_cfg_csv_filename, exp_filename_csv):
    # Check CfgProj values
    assert cfg_loc.filename == exp_cfg_filename
    assert exists(cfg_loc.filename), f'CFG NOT EXIST({cfg_loc.filename})'
    ntcfg = read_config(cfg_loc.filename)
    docproj = DocProj(ntcfg.doc, cfg_loc.filename)
    assert docproj.project == project, (f'ACT({docproj.project}) != EXP({project})\n'
        f'{str_file(cfg_loc.filename, msg=cfg_loc.filename)}')
    assert docproj.csv_filename == exp_cfg_csv_filename, \
        f"ACT({docproj.csv_filename}) != EXP({exp_cfg_csv_filename})"
    act_csv = cfg_loc.get_filename_csv(user)
    print(act_csv)
    assert act_csv == exp_filename_csv
    return docproj


if __name__ == '__main__':
    test_cmd_init()
