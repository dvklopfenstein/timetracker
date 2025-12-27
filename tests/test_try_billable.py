#!/usr/bin/env python3
"""Test adding 'Billable' tag, if specified in args"""

from os import environ
from timetracker.cli.cli import Cli
from timetracker.cmd.common import add_tag_billable


def test_try_billable(username='researcher'):
    """Test adding 'Billable' to tags"""
    username = environ.get('USER', username)
    _test_billable0tags0(username)
    _test_billable1tags0(username)
    _test_billable0tags1(username)
    _test_billable1tags1(username)
    _test_billable0tags2(username)
    _test_billable1tags2a(username)
    _test_billable1tags2b(username)


def _test_billable0tags0(username):
    args = ['stop', '-m', 'Not marked billable; no other tags']
    cli = Cli(username, args)
    _try_billable(cli.args, cli.args.billable)
    assert cli.args.tags is None
    assert not cli.args.billable
    _prt(args, cli)

def _test_billable1tags0(username):
    args = ['stop', '-b', '-m', 'Marked billable; no other tags']
    cli = Cli(username, args)
    _try_billable(cli.args, cli.args.billable)
    assert cli.args.tags == ['Billable']
    assert cli.args.billable
    _prt(args, cli)

def _test_billable0tags1(username):
    args = ['stop', '-t', 'tag1', '-m', 'Not marked billable; no other tags']
    cli = Cli(username, args)
    _try_billable(cli.args, cli.args.billable)
    assert cli.args.tags == ['tag1']
    assert not cli.args.billable
    _prt(args, cli)

def _test_billable1tags1(username):
    args = ['stop', '-t', 'tag1', '-b', '-m', 'Marked billable; no other tags']
    cli = Cli(username, args)
    _try_billable(cli.args, cli.args.billable)
    assert cli.args.tags == ['tag1', 'Billable']
    assert cli.args.billable
    _prt(args, cli)

def _test_billable0tags2(username):
    args = ['stop', '-t', 'tag1', 'tag2', '-m', 'Not marked billable; no other tags']
    cli = Cli(username, args)
    _try_billable(cli.args, cli.args.billable)
    assert cli.args.tags == ['tag1', 'tag2'], cli.args.tags
    assert not cli.args.billable
    _prt(args, cli)

def _test_billable1tags2a(username):
    """Tags cannot be specified as: -t tag1 -t tag2"""
    args = ['stop', '-t', 'tag1', '-t', 'tag2', '-b', '-m', 'Marked billable; no other tags']
    cli = Cli(username, args)
    _try_billable(cli.args, cli.args.billable)
    assert cli.args.tags == ['tag2', 'Billable'], cli.args.tags
    assert cli.args.billable
    _prt(args, cli)

def _test_billable1tags2b(username):
    """Tags must be specified as: -t tag1 tag2"""
    args = ['stop', '-t', 'tag1', 'tag2', '-b', '-m', 'Marked billable; no other tags']
    cli = Cli(username, args)
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
