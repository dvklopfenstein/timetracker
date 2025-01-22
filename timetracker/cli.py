"""Command line interface (CLI) for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import environ
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter


class Cli:
    """Command line interface (CLI) for timetracking"""
    # pylint: disable=too-few-public-methods

    defaults = {
        'init': './.timetracker',
    }

    def __init__(self, cfgfile=None):
        self.cfgfile = cfgfile
        self.parser = self._init_parsers()

    def get_args(self):
        """Get arguments for ScriptFrame"""
        args = self.parser.parse_args()
        print(f'DVK ARGS: {args}')
        return args

    def _init_parsers(self):
        parser = self._init_parser()
        self._add_subparsers(parser)
        return parser

    def _init_parser(self):
        parser = ArgumentParser(
            prog='timetracker',
            description="Track your time in git-managed repos",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        parser.add_argument('directory', nargs='?',
            default=self.defaults['init'],
            help='Directory to hold timetracking data')
        parser.add_argument('-n', '--name',
            default=environ.get('USER', 'person1'),
            help='Name for timetracking')
        return parser

    def _add_subparsers(self, parser):
        # Subparsers
        subparsers = parser.add_subparsers(dest='command',
            help='timetracker subcommand help')
        self._add_subparser_init(subparsers)
        self._add_subparser_start(subparsers)
        self._add_subparser_stop(subparsers)

    def _add_subparser_init(self, subparsers):
        parser = subparsers.add_parser(name='init',
            help='Initialize the .timetracking directory',
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        return parser

    def _add_subparser_start(self, subparsers):
        parser = subparsers.add_parser(name='start',
            help='Start timetracking')
        return parser

    def _add_subparser_stop(self, subparsers):
        parser = subparsers.add_parser(name='stop',
            help='Stop timetracking')
        return parser


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
