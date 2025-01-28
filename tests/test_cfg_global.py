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
#from timetracker.cli import Cli
#from timetracker.filemgr import FileMgr
#from timetracker.cfg.cfg_global import CfgGlobal

basicConfig(level=DEBUG)


def test_cfgbase_home():
    """Test instantiating a default CfgGlobal"""
    cfg = CfgGlobal()
    assert cfg.fname == join(expanduser('~'), '.timetrackerconfig')
    assert cfg.docini['projects'] == []
    #system(f'cat {cfg.fname}')

def test_cfgbase_temp():
    """Test cfg flow"""
    # 1) INITIALIZE "HOME" DIRECTORY
    with TemporaryDirectory() as tmp_home:
        cfg = CfgGlobal(tmp_home)
        assert cfg.fname == join(tmp_home, '.timetrackerconfig'), f'{cfg.fname}'
        assert cfg.docini['projects'] == []
        # 2) WRITE AN EMPTY GLOBAL CONFIGURATION FILE
        cfg.wr_cfg()
        #debug(run(f'find {tmp_home}'.split(), capture_output=True, text=True, check=True).stdout)
        # 3) READ THE EMPTY GLOBAL CONFIGURATION FILE
        doc = cfg.rd_cfg()
        assert doc['projects'] == cfg.docini['projects']
        debug(run(f'cat {cfg.fname}'.split(), capture_output=True, text=True, check=True).stdout)
        # 4) Create local project directories
        _mk_dirs(tmp_home)


def test_cfgdir():
    """Test the TimeTracker global configuration"""
    cfg = CfgGlobal()
    assert dirname(cfg.fname) == expanduser('~')

    with TemporaryDirectory() as tmp_home:
        cfg = CfgGlobal(cfgdir=tmp_home.name)
        assert dirname(cfg.fname) == tmp_home.name
        tmp_home.cleanup()

def _mk_dirs(tmp_home):
    projs = {
        'proja' : join(tmp_home.name, 'proj/apples'),
        'projb' : join(tmp_home.name, 'proj/blueberries'),
        'projc' : join(tmp_home.name, 'proj/cacao'),
    }
    for pdir in projs.values():
        makedirs(pdir)
    debug(run(f'find {tmp_home.name}'.split(), capture_output=True, text=True, check=True).stdout)

if __name__ == '__main__':
    #test_cfgdir()
    #test_cfgbase_home()
    test_cfgbase_temp()
