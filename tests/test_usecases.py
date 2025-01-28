#!/usr/bin/env python3
"""Test the TimeTracker configuration"""

from sys import argv
from os import environ
##from os import getcwd
from collections import namedtuple
from datetime import timedelta
from timeit import default_timer
from timetracker.cfg.cfg import Cfg
from timetracker.cli import Cli
from timetracker.filemgr import FileMgr
from timetracker.cfg.cfg_global import CfgGlobal

# pylint: disable=fixme

def test_cfg():
    """Test the TimeTracker configuration"""

    tic = default_timer()
    # `$ trk`
    _trk()
    #_trk_help()
    print(str(timedelta(seconds=default_timer()-tic)))

def test_basic():
    """Test the basic timetracker flow"""
    _trk_init_help()
    _trk_init()
    _trk_start()
    _trk_stop()

def test_dir():
    """Test the basic timetracker flow"""
    mainargs = '-d .tt'.split()
    nta = _trk_init(mainargs)
    assert nta.args.directory == '.tt'
    nta = _trk_start(mainargs)
    assert nta.args.directory == '.tt'
    nta = _trk_stop(mainargs)
    assert nta.args.directory == '.tt'

# ------------------------------------------------------------
def _trk_stop(mainargs=None):
    """`$ trk stop -m 'Test stopping the timer'"""
    if not mainargs:
        mainargs = []
    nta = _get_nttrkr(mainargs + ['stop', '-m', 'Test stopping the timer'])
    assert nta.args.command == 'stop'
    return nta

def _trk_start(mainargs=None):
    """`$ trk start"""
    if not mainargs:
        mainargs = []
    nta = _get_nttrkr(mainargs + ['start'])
    assert nta.args.command == 'start'
    return nta

def _trk_init(mainargs=None):
    """`$ trk init"""
    if not mainargs:
        mainargs = []
    nta = _get_nttrkr(mainargs + ['init'])
    assert nta.args.command == 'init'
    return nta

def _trk_init_help(mainargs=None):
    """`$ trk init"""
    if not mainargs:
        mainargs = []
    nta = _get_nttrkr(mainargs + 'init --help'.split())
    assert nta.args.command == 'init'
    return nta

def _trk_help():
    """`$ trk --help`"""
    nta = _get_nttrkr(['--help'])
    assert nta
    # TODO: Check that help message was printed

def _trk():
    """`$ trk"""
    nta = _get_nttrkr([])
    # TODO: Check that help message was printed
    # TODO: Check: Run `trk init` to initialize local timetracker
    assert nta.args.directory == Cfg.DIR
    assert nta.args.name == environ['USER']
    assert not nta.args.quiet
    assert nta.args.command is None

def _get_nttrkr(arglist):
    cfg = Cfg()
    cli = Cli(cfg)
    print(f'DDDDDDDDDDDDDDDDDDD {argv}')
    args = cli.get_args_test(arglist)
    cfg_global = CfgGlobal()
    print(f'TEST ARGS: {args}')
    fmgr = FileMgr(cfg, cfg_global, **vars(args))
    nto = namedtuple('TestTrkr', 'args fmgr')
    return nto(args=args, fmgr=fmgr)

if __name__ == '__main__':
    #test_cfg()
    #test_basic()
    test_dir()
