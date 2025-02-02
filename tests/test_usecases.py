#!/usr/bin/env python3
"""Test the TimeTracker configuration"""

from os import environ
from datetime import timedelta
from timeit import default_timer
from timetracker.cfg.finder import CfgFinder
from timetracker.cli import Cli

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
    mainargs = '--trksubdir .tt'.split()
    args = _trk_init(mainargs)
    assert args.trksubdir == '.tt'
    args = _trk_start(mainargs)
    assert args.trksubdir == '.tt'
    args = _trk_stop(mainargs)
    assert args.trksubdir == '.tt'

# ------------------------------------------------------------
def _trk_stop(mainargs=None):
    """`$ trk stop -m 'Test stopping the timer'"""
    if not mainargs:
        mainargs = []
    args = _parse_args(mainargs + ['stop', '-m', 'Test stopping the timer'])
    assert args.command == 'stop'
    return args

def _trk_start(mainargs=None):
    """`$ trk start"""
    if not mainargs:
        mainargs = []
    args = _parse_args(mainargs + ['start'])
    assert args.command == 'start'
    return args

def _trk_init(mainargs=None):
    """`$ trk init"""
    if not mainargs:
        mainargs = []
    args = _parse_args(mainargs + ['init'])
    assert args.command == 'init'
    return args

def _trk_init_help(mainargs=None):
    """`$ trk init"""
    if not mainargs:
        mainargs = []
    args = _parse_args(mainargs + 'init --help'.split())
    assert args.command == 'init'
    return args

def _trk_help():
    """`$ trk --help`"""
    args = _parse_args(['--help'])
    assert args
    # TODO: Check that help message was printed

def _trk():
    """`$ trk"""
    args = _parse_args([])
    # TODO: Check that help message was printed
    # TODO: Check: Run `trk init` to initialize local timetracker
    assert args.trksubdir == CfgFinder.DIRTRK
    assert args.name == environ['USER']
    assert not args.quiet
    assert args.command is None

def _parse_args(arglist):
    cli = Cli()
    print(f'RESEARCHER  ARGS: {arglist}')
    args = cli.get_args_test(arglist)
    print(f'TEST ARGS: {args}\n')
    return args

if __name__ == '__main__':
    #test_cfg()
    #test_basic()
    test_dir()
