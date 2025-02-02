"""Command line interface (CLI) for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import argv
from sys import exit as sys_exit
from os.path import normpath
from os.path import relpath
from logging import debug
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from argparse import SUPPRESS
from timetracker import __version__


class Cli:
    """Command line interface (CLI) for timetracking"""

    def __init__(self, cfg_proj):
        self.cfg_proj = cfg_proj
        self.parser = self._init_parsers()
        self.argv_tests = {
            'directory': set(['-d', '--directory']),
        }

    def get_args_cli(self):
        """Get arguments for ScriptFrame"""
        args = self.parser.parse_args()
        self._adjust_args(args)
        debug(f'TIMETRACKER ARGS: {args}')
        if args.version:
            print(f'trk {__version__}')
            sys_exit()
        return args

    def get_args_test(self, arglist):
        """Get arguments for ScriptFrame"""
        args = self.parser.parse_args(arglist)
        self._adjust_args(args)
        print(f'TIMETRACKER ARGS: {args}')
        if args.version:
            print(f'trk {__version__}')
            sys_exit()
        return args

    def _adjust_args(self, args):
        """Replace config default values with researcher-specified values"""
        debug(f'ARGV: {argv}')
        argv_set = set(argv)
        # If researcher set a proj dir other than ./timetracker, use it
        if not argv_set.isdisjoint(self.argv_tests['directory']):
            self.cfg_proj.workdir = args.directory
        # pylint: disable=fixme
        # TODO: CHeck if cvs.directory is being changed
        return args

    # -------------------------------------------------------------------------------
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
        cfg = self.cfg_proj
        parser.add_argument('-d', '--directory', metavar='DIR', default=cfg.DIR,
            # Directory that holds the local project config file
            help=SUPPRESS)
        parser.add_argument('-n', '--username', metavar='NAME', dest='name', default=cfg.name,
            help="A person's alias for timetracking")
        parser.add_argument('-q', '--quiet', action='store_true',
            help='Only print error and warning messages; information will be suppressed.')
        parser.add_argument('--version', action='store_true',
            help='Print the timetracker version')
        return parser

    def _add_subparsers(self, parser):
        # Subparsers
        subparsers = parser.add_subparsers(dest='command', help='timetracker subcommand help')
        self._add_subparser_init(subparsers)
        self._add_subparser_start(subparsers)
        self._add_subparser_restart(subparsers)
        self._add_subparser_stop(subparsers)
        self._add_subparser_csvupdate(subparsers)
        self._add_subparser_files(subparsers)

    # -------------------------------------------------------------------------------
    def _add_subparser_restart(self, subparsers):
        # pylint: disable=fixme
        # TODO: add a command that restarts the timers using the last csv time entry
        #   * Add --verbose to print which files are edited and the csv message
        #   * re-write the start file
        #   * remove the last csv entry
        pass

    def _add_subparser_files(self, subparsers):
        # pylint: disable=fixme
        # TODO: add a command that lists timetracker files:
        #  * csv file
        #  * start file, if it exists (--verbose)
        #  * local cfg file
        #  * global cfg file
        pass

    def _add_subparser_init(self, subparsers):
        parser = subparsers.add_parser(name='init',
            help='Initialize the .timetracking directory',
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        cfg = self.cfg_proj
        parser.add_argument('--csvdir', default=normpath(relpath(cfg.dir_csv)),
            help='Directory for csv files storing start and stop times')
        parser.add_argument('-p', '--project', default=cfg.project,
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

    def _add_subparser_csvupdate(self, subparsers):
        parser = subparsers.add_parser(name='csvupdate',
            help='Update values in csv columns containing weekday, am/pm, and duration',
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        parser.add_argument('-f', '--force', action='store_true',
            help='Over-write the csv indicated in the project `config` by `filename`')
        parser.add_argument('-i', '--input', metavar='file.csv',
            help='Specify an input csv file')
        parser.add_argument('-o', '--output', metavar='file.csv', default='updated.csv',
            help='Specify an output csv file')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
