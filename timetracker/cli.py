"""Command line interface (CLI) for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import walk
from os.path import isdir
from os.path import normpath
from sys import exit as sys_exit
from logging import error
from argparse import ArgumentParser
from timetracker.recorder import Recorder


def main():
    """Command line interface (CLI) for timetracking"""
    cli = Cli()
    args = cli.get_args()
    #rec = Recorder()


class Cli:
    """Command line interface (CLI) for timetracking"""
    # pylint: disable=too-few-public-methods

    #def __init__(self):

    def get_args(self):
        """Get arguments for ScriptFrame"""
        parser = self._get_parser()
        args = parser.parse_args()
        print(f'ARGS: {args}')
        return args

    def _get_parser(self):
        parser = ArgumentParser(
            prog='timetracker',
            description="Track your time in git-managed repos",
        )
        subparsers = parser.add_subparsers(help='timetracker subcommand help')
        parser_ini = subparsers.add_parser('init', help='Initialize timetracking')
        parser_start = subparsers.add_parser('start', help='Start timetracking')
        parser_stop = subparsers.add_parser('stop', help='Stop timetracking')
        return parser


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
