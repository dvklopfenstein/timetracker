#!/usr/bin/env python3
"""Test the TimeTracker configuration"""

from os import environ
from os import getcwd
from collections import namedtuple
from datetime import timedelta
from timeit import default_timer
from timetracker.cfg import Cfg
from timetracker.cli import Cli
from timetracker.filemgr import FileMgr


def test_cfg():
    """Test the TimeTracker configuration"""

    tic = default_timer()
    # `$ trk`
    _trk()
    #_trk_help()
    print(str(timedelta(seconds=default_timer()-tic)))

def test_basic():
    """Test the basic timetracker flow"""
    _trk_init()
    _trk_start()
    _trk_stop()

def _trk_stop():
    """`$ trk stop -m 'Test stopping the timer'"""
    nta = _get_nttrkr(['stop', '-m', 'Test stopping the timer'])
    assert nta.args.command == 'stop'

def _trk_start():
    """`$ trk start"""
    nta = _get_nttrkr(['start'])
    assert nta.args.command == 'start'

def _trk_init():
    """`$ trk init"""
    nta = _get_nttrkr(['init'])
    assert nta.args.command == 'init'

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
    assert nta.args.directory == './.timetracker'
    assert nta.args.name == environ['USER']
    assert not nta.args.quiet
    assert nta.args.command is None

def _get_nttrkr(arglist):
    cli = Cli()
    args = cli.get_args_test(arglist)
    print(f'TEST ARGS: {args}')
    fmgr = FileMgr(**vars(args))
    nto = namedtuple('TestTrkr', 'args fmgr')
    return nto(args=args, fmgr=fmgr)

if __name__ == '__main__':
    test_cfg()
    test_basic()
