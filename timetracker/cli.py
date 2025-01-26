"""Command line interface (CLI) for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import argv
from os.path import normpath
from os.path import relpath
from logging import debug
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from argparse import SUPPRESS


class Cli:
    """Command line interface (CLI) for timetracking"""

    def __init__(self, cfg):
        self.cfg = cfg
        self.parser = self._init_parsers()

    def get_args_cli(self):
        """Get arguments for ScriptFrame"""
        args = self.parser.parse_args()
        self._adjust_args(args)
        debug(f'TIMETRACKER ARGS: {args}')
        return args

    def get_args_test(self, arglist):
        """Get arguments for ScriptFrame"""
        args = self.parser.parse_args(arglist)
        self._adjust_args(args)
        print(f'TIMETRACKER ARGS: {args}')
        return args

    def _adjust_args(self, args):
        debug(f'ARGV: {argv}')
        if args.command == 'init':
            self.cfg.update_init(args.project, args.csvdir)
            debug(self.cfg.str_cfg())
        return args

    def _init_parsers(self):
        parser = self._init_parser_top()
        self._add_subparsers(parser)
        return parser

    def _init_parser_top(self):
        parser = ArgumentParser(
            prog='timetracker',
            description="Track your time repo by repo",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        cfg = self.cfg
        parser.add_argument('-d', metavar='DIRECTORY', dest='directory', default=cfg.DIR,
            help='Directory that holds the local config file')
        parser.add_argument('-n', '--name', default=cfg.name,
            help="A person's alias for timetracking")
        parser.add_argument('-q', '--quiet', action='store_true',
            help='Only print error and warning messages; information will be suppressed.')
        return parser

    def _add_subparsers(self, parser):
        # Subparsers
        subparsers = parser.add_subparsers(dest='command', help='timetracker subcommand help')
        self._add_subparser_init(subparsers)
        self._add_subparser_start(subparsers)
        self._add_subparser_stop(subparsers)

    def _add_subparser_init(self, subparsers):
        parser = subparsers.add_parser(name='init',
            help='Initialize the .timetracking directory',
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        cfg = self.cfg
        parser.add_argument('--csvdir', default=normpath(relpath(cfg.dir_csv)),
            help='Directory for csv files storing start and stop times')
        parser.add_argument('-p', metavar='PROJECT', dest='project', default=cfg.project,
            help="The name of the project to be time tracked")
        return parser

    def _add_subparser_start(self, subparsers):
        parser = subparsers.add_parser(name='start', help='Start timetracking')
        # Test feature: Force over-writing of start time
        parser.add_argument('-f', '--force', action='store_true',
            help=SUPPRESS)
        return parser

    def _add_subparser_stop(self, subparsers):
        parser = subparsers.add_parser(name='stop', help='Stop timetracking')
        parser.add_argument('-m', '--message', required=True,
            help='Message describing the work done in the time unit')
        parser.add_argument('--activity', default='',
            help='Activity for time unit')
        parser.add_argument('-t', '--tags', nargs='*',
            help='Tags for this time unit')
        parser.add_argument('-k', '--keepstart', action='store_true', default=False,
            #help='Resetting the timer is the normal behavior; Keep the start time this time')
            help=SUPPRESS)
        return parser


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
