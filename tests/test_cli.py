#!/usr/bin/env python3
"""Test the TimeTracker configuration"""

from os import environ
from datetime import timedelta
from timeit import default_timer
from pytest import raises
from timetracker.consts import DIRTRK
from timetracker.cli import Cli

# pylint: disable=fixme

# TODO:
# trk
# trk start
# exp: Please init timer

def test_cfg():
    """Test the TimeTracker configuration"""
    tic = default_timer()
    # `$ trk`
    _trk()
    #_trk_help()
    print(str(timedelta(seconds=default_timer()-tic)))

def test_basic():
    """Test the basic timetracker flow"""
    with raises(SystemExit) as excinfo:
        _trk_init_help()
    assert excinfo.value.code == 0
    _trk_init()
    _trk_start()
    _trk_stop()

def test_dir():
    """Test the basic timetracker flow"""
    mainargs = '--trk-dir .tt'.split()
    args = _trk_init(mainargs)
    assert args.trk_dir == '.tt'
    args = _trk_start(mainargs)
    assert args.trk_dir == '.tt'
    args = _trk_stop(mainargs)
    assert args.trk_dir == '.tt'

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
    assert args.trk_dir == DIRTRK
    assert args.name == environ['USER']
    assert args.command is None

def _parse_args(arglist):
    print(f'RESEARCHER  ARGS: {arglist}')
    cli = Cli(arglist)
    print(f'TEST ARGS: {cli.args}\n')
    return cli.args

if __name__ == '__main__':
    test_cfg()
    #test_basic()
    #test_dir()
