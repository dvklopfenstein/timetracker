"""Command line interface (CLI) for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from logging import error
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter


class Cli:
    """Command line interface (CLI) for timetracking"""
    # pylint: disable=too-few-public-methods

    def __init__(self, cfgfile):
        self.cfgfile = cfgfile
        self.parser = self._init_parser()

    def get_args(self):
        """Get arguments for ScriptFrame"""
        args = self.parser.parse_args()
        print(f'ARGS: {args}')
        self._chkargs(args)
        return args

    def _init_parser(self):
        parser = ArgumentParser(
            prog='timetracker',
            description="Track your time in git-managed repos",
        )
        subparsers = parser.add_subparsers(dest='command',
            help='timetracker subcommand help')
        self._add_parser_init(subparsers)
        self._add_parser_start(subparsers)
        self._add_parser_stop(subparsers)
        return parser

    def _add_parser_init(self, subparsers):
        parser = subparsers.add_parser(name='init',
            help='Initialize the .timetracking directory',
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        parser.add_argument('directory', nargs='?', default='./.timetracker',
            help='Optional user specified directory')
        return parser

    def _add_parser_start(self, subparsers):
        parser = subparsers.add_parser(name='start',
            help='Start timetracking')
        return parser

    def _add_parser_stop(self, subparsers):
        parser = subparsers.add_parser(name='stop',
            help='Stop timetracking')
        return parser

    def _chkargs(self, args):
        if args.command is None:
            if self.cfgfile is None:
                self.parser.print_help()
                print('')
                error('Use `trkr init` to initialize '
                     'a timetracker config file')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
