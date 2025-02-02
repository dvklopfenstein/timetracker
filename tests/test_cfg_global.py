#!/usr/bin/env python3
"""Test the TimeTracker global configuration"""

#from sys import argv
#from os import environ
###from os import getcwd
from os import makedirs
##from os.path import exists
from os.path import join
from os.path import dirname
from os.path import expanduser
from subprocess import run
#from collections import namedtuple
#from datetime import timedelta
#from timeit import default_timer
from logging import basicConfig
from logging import DEBUG
from logging import debug
from tempfile import TemporaryDirectory
from timetracker.cfg.cfg_global import CfgGlobal
from timetracker.cfg.cfg_local import CfgProj
from timetracker.cfg.utils import get_relpath_adj
#from timetracker.cli import Cli
#from timetracker.cfg.cfg_global import CfgGlobal

basicConfig(level=DEBUG)


def test_cfgbase_home():
    """Test instantiating a default CfgGlobal"""
    cfg = CfgGlobal()
    assert cfg.fname == join(expanduser('~'), '.timetrackerconfig')
    assert cfg.doc['projects'] == []
    #system(f'cat {cfg.fname}')

def test_cfgbase_temp():
    """Test cfg flow"""
    sep = f'{"-"*80}\n'
    print(f'{sep}1) INITIALIZE "HOME" DIRECTORY')
    with TemporaryDirectory() as tmp_home:
        cfgtop = CfgGlobal(tmp_home)
        assert cfgtop.fname == join(tmp_home, '.timetrackerconfig'), f'{cfgtop.fname}'
        assert cfgtop.doc['projects'] == []
        print(f'{sep}2) WRITE AN EMPTY GLOBAL CONFIGURATION FILE')
        cfgtop.wr_cfg()
        print(f'{sep}3) READ THE EMPTY GLOBAL CONFIGURATION FILE')
        doc = cfgtop.rd_cfg()
        assert doc is not None
        # pylint: disable=unsubscriptable-object
        assert doc['projects'] == cfgtop.doc['projects']
        #debug(f"XXXXX {doc['projects']}")
        #debug(f"YYYYY {cfgtop.doc['projects']}")
        assert doc['projects'] == cfgtop.doc['projects']
        _run(f'cat {cfgtop.fname}')
        print(f'{sep}4) Create local project directories')
        proj2wdir = _mk_dirs(tmp_home)
        _find(tmp_home)
        print(f'{sep}5) Create a local cfg object for the apples project')
        name = 'tester'
        exp_projs = []
        for proj, projdir in proj2wdir.items():
            print(f'{sep}ADD PROJECT({proj}): {projdir}')
            workdir = join(projdir, '.timetracker')
            # cfgname_proj = /tmp/tmptrz29mh6/proj/apples/.timetracker/config
            cfgname_proj = join(workdir, 'config')
            # EXP: apples '~/proj/apples/.timetracker/config'
            exp_projs.append([proj, get_relpath_adj(cfgname_proj, tmp_home)])
            # INIT LOCAL PROJECT CONFIG
            cfgloc = CfgProj(workdir, proj, name)
            assert cfgloc.workdir == workdir
            assert cfgloc.project == proj
            assert cfgloc.name == name
            cfgloc.mk_workdir()
            cfgloc.wr_cfg()
            # cat project/.timetracker/config
            fnamecfg_proj = cfgloc.get_filename_cfglocal()
            debug(f'PROJ CFG: {fnamecfg_proj}')
            _run(f'cat {fnamecfg_proj}')
            # ADD PROJECT TO GLOBAL CONFIG AND WRITE
            cfgtop.add_proj(proj, fnamecfg_proj)
            assert cfgtop.doc["projects"].unwrap() == exp_projs, (
                'UNEXPECTED PROJS:\n'
                f'EXP({exp_projs})\n'
                f'ACT({cfgtop.doc["projects"].unwrap()})')
            cfgtop.wr_cfg()
            _run(f'cat {cfgtop.fname}')
            _find(workdir)



def test_dirhome():
    """Test the TimeTracker global configuration"""
    cfg = CfgGlobal()
    assert dirname(cfg.fname) == expanduser('~')

    with TemporaryDirectory() as tmp_home:
        cfg = CfgGlobal(dirhome=tmp_home.name)
        assert dirname(cfg.fname) == tmp_home.name
        tmp_home.cleanup()

def _mk_dirs(tmp_home):
    projs = {
        'apples'      : join(tmp_home, 'proj/apples'),
        'blueberries' : join(tmp_home, 'proj/blueberries'),
        'cacao'       : join(tmp_home, 'proj/cacao'),
    }
    for pdir in projs.values():
        makedirs(pdir)
    return projs

def _run(cmd):
    debug(run(cmd.split(), capture_output=True, text=True, check=True).stdout)

def _find(home):
    debug(run(f'find {home}'.split(), capture_output=True, text=True, check=True).stdout)

if __name__ == '__main__':
    #test_dirhome()
    #test_cfgbase_home()
    test_cfgbase_temp()
