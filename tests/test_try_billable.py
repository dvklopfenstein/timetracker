#!/usr/bin/env python3
"""Test adding 'Billable' tag, if specified in args"""

from timetracker.cli import Cli
from timetracker.cmd.common import add_tag_billable


def test_try_billable():
    """Test adding 'Billable' to tags"""
    _test_billable0tags0()
    _test_billable1tags0()
    _test_billable0tags1()
    _test_billable1tags1()
    _test_billable0tags2()
    _test_billable1tags2a()
    _test_billable1tags2b()


def _test_billable0tags0():
    args = ['stop', '-m', 'Not marked billable; no other tags']
    cli = Cli(args)
    _try_billable(cli.args, cli.args.billable)
    assert cli.args.tags is None
    assert not cli.args.billable
    _prt(args, cli)

def _test_billable1tags0():
    args = ['stop', '-b', '-m', 'Marked billable; no other tags']
    cli = Cli(args)
    _try_billable(cli.args, cli.args.billable)
    assert cli.args.tags == ['Billable']
    assert cli.args.billable
    _prt(args, cli)

def _test_billable0tags1():
    args = ['stop', '-t', 'tag1', '-m', 'Not marked billable; no other tags']
    cli = Cli(args)
    _try_billable(cli.args, cli.args.billable)
    assert cli.args.tags == ['tag1']
    assert not cli.args.billable
    _prt(args, cli)

def _test_billable1tags1():
    args = ['stop', '-t', 'tag1', '-b', '-m', 'Marked billable; no other tags']
    cli = Cli(args)
    _try_billable(cli.args, cli.args.billable)
    assert cli.args.tags == ['tag1', 'Billable']
    assert cli.args.billable
    _prt(args, cli)

def _test_billable0tags2():
    args = ['stop', '-t', 'tag1', 'tag2', '-m', 'Not marked billable; no other tags']
    cli = Cli(args)
    _try_billable(cli.args, cli.args.billable)
    assert cli.args.tags == ['tag1', 'tag2'], cli.args.tags
    assert not cli.args.billable
    _prt(args, cli)

def _test_billable1tags2a():
    """Tags cannot be specified as: -t tag1 -t tag2"""
    args = ['stop', '-t', 'tag1', '-t', 'tag2', '-b', '-m', 'Marked billable; no other tags']
    cli = Cli(args)
    _try_billable(cli.args, cli.args.billable)
    assert cli.args.tags == ['tag2', 'Billable'], cli.args.tags
    assert cli.args.billable
    _prt(args, cli)

def _test_billable1tags2b():
    """Tags must be specified as: -t tag1 tag2"""
    args = ['stop', '-t', 'tag1', 'tag2', '-b', '-m', 'Marked billable; no other tags']
    cli = Cli(args)
    _try_billable(cli.args, cli.args.billable)
    assert cli.args.tags == ['tag1', 'tag2', 'Billable'], cli.args.tags
    assert cli.args.billable
    _prt(args, cli)

def _prt(args, cli):
    print(f'ARGS:   {" ".join(args)}')
    print(f'RESULT: billable={cli.args.billable}, tags={cli.args.tags}')
    print('')

def _try_billable(args, billable):
    if not billable:
        return
    add_tag_billable(args)


if __name__ == '__main__':
    test_try_billable()
