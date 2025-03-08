"""Command line interface (CLI) for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import argv as sys_argv
from sys import exit as sys_exit
from os import getcwd
from os.path import exists
from logging import debug

from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from argparse import SUPPRESS
from timetracker import __version__
from timetracker.fncs import FNCS
from timetracker.cfg.utils import get_username
from timetracker.cfg.finder import CfgFinder
from timetracker.cfg.cfg_local import CfgProj
from timetracker.cmd.none import cli_run_none


def main():
    """Connect all parts of the timetracker"""
    #from logging import basicConfig, DEBUG
    #basicConfig(level=DEBUG)
    obj = Cli()
    obj.run()


class Cli:
    """Command line interface (CLI) for timetracking"""
    # pylint: disable=too-few-public-methods

    ARGV_TESTS = {
        'trksubdir': set(['--trksubdir']),
    }

    def __init__(self, args=None):
        sysargs = self._adjust_args(args)
        self.finder = CfgFinder(getcwd(), self._init_trksubdir())
        self.fcfg = self.finder.get_cfgfilename()
        self.user = get_username()  # default username
        self.fcsv = CfgProj(self.fcfg).get_filename_csv() if exists(self.fcfg) else None
        self.parser = self._init_parser_top('timetracker')
        self.args = self._init_args(sysargs)

    def run(self):
        """Run timetracker"""
        debug(f'Cli RUNNNNNNNNNNNNNNNNNN ARGS: {self.args}')
        debug(f'Cli RUNNNNNNNNNNNNNNNNNN DIRTRK:  {self.finder.get_dirtrk()}')
        debug(f'Cli RUNNNNNNNNNNNNNNNNNN CFGNAME: {self.fcfg}')
        if self.args.command is not None:
            FNCS[self.args.command](self.fcfg, self.args)
        else:
            cli_run_none(self.fcfg, self.args)

    def _adjust_args(self, given_args):
        """Replace config default values with researcher-specified values"""
        debug(f'ARGV: {sys_argv}')
        ret = []
        args = sys_argv[1:] if given_args is None else given_args
        optname = None
        for elem in args:
            if optname == '--at':
                #debug(f' --at opt was({elem})')
                elem = self._adjust_opt_at(elem)
                #debug(f' --at opt now({elem})')
                optname = None
            ret.append(elem)
            if elem == '--at':
                optname = elem
            #debug(f'ADJUST_ARGS>>({elem})')
        return ret

    @staticmethod
    def _adjust_opt_at(val):
        if val[:1] != '-':
            return val
        return val if val[1:2] == ' ' else ' ' + val

    def _init_args(self, arglist):
        """Get arguments for ScriptFrame"""
        args = self.parser.parse_args(arglist)
        debug(f'TIMETRACKER ARGS: {args}')
        if args.version:
            print(f'trk {__version__}')
            sys_exit(0)
        return args

    def _init_trksubdir(self):
        found = False
        for arg in sys_argv:
            if found:
                debug(f'Cli FOUND: argv --trksubdir {arg}')
                return arg
            if arg == '--trksubdir':
                found = True
        return None

    @staticmethod
    def _get_cmds():
        """In ArgumentParser, usage=f'%(prog)s [-h] {self._get_cmds()}'"""
        # parser.add_subparsers(dest='command', metavar=self._get_cmds(), help=SUPPRESS)
        cmds = ','.join(k for k in FNCS if k != 'invoice')
        return f'{{{cmds}}}'

    # -------------------------------------------------------------------------------
    def _init_parser_top(self, progname):
        """Create the top-level parser"""
        parser = ArgumentParser(
            prog=progname,
            description="Track your time repo by repo",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        parser.add_argument('--trksubdir', metavar='DIR', default=self.finder.trksubdir,
            # Directory that holds the local project config file
            help='Directory that holds the local project config file')
            #help=SUPPRESS)
        parser.add_argument('-u', '--username', metavar='NAME', dest='name', default=self.user,
            help="A person's alias or username for timetracking")
        parser.add_argument('-q', '--quiet', action='store_true',
            help='Only print error and warning messages; information will be suppressed.')
        parser.add_argument('--version', action='store_true',
            help='Print the timetracker version')
        self._add_subparsers(parser)
        return parser

    def _add_subparsers(self, parser):
        subparsers = parser.add_subparsers(dest='command')
        self._add_subparser_init(subparsers)
        self._add_subparser_start(subparsers)
        self._add_subparser_stop(subparsers)
        self._add_subparser_cancel(subparsers)
        self._add_subparser_time(subparsers)
        self._add_subparser_report(subparsers)
        self._add_subparser_csv(subparsers)
        self._add_subparser_csvupdate(subparsers)
        #help='timetracker subcommand help')
        ##self._add_subparser_files(subparsers)
        ##return parser

    # -------------------------------------------------------------------------------
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
            formatter_class=ArgumentDefaultsHelpFormatter)
        # DEFAULTS: dir_csv project
        parser.add_argument('--csvdir',
            default=self.finder.get_dircsv_default(),
            help='Directory for csv files storing start and stop times')
        parser.add_argument('-p', '--project', default=self.finder.project,
            help="The name of the project to be time tracked")
        return parser

    @staticmethod
    def _add_subparser_start(subparsers):
        parser = subparsers.add_parser(name='start', help='start timetracking')
        # test feature: force over-writing of start time
        parser.add_argument('-f', '--force', action='store_true',
            help='Force restart timer now or `--at` a specific or elapsed time')
        parser.add_argument('--at', metavar='time',
            help='start tracking at a '
                 'specific(ex: 4pm, "Tue 4pm") or '
                 'elapsed time(ex: 10min, ~10min, 4hr)')
        return parser

    @staticmethod
    def _add_subparser_stop(subparsers):
        parser = subparsers.add_parser(name='stop',
            help='Stop timetracking',
            formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-m', '--message', required=True, metavar='TXT',
            help='Message describing the work done in the time unit')
        parser.add_argument('--activity', default='',
            help='Activity for time unit')
        parser.add_argument('-t', '--tags', nargs='*',
            help='Tags for this time unit')
        parser.add_argument('-k', '--keepstart', action='store_true', default=False,
            #help='Resetting the timer is the normal behavior; Keep the start time this time')
            help=SUPPRESS)
        parser.add_argument('--at', metavar='time',
            help='start tracking at a '
                 'specific(ex: 4pm, "2025-01-05 04:30pm") or '
                 'elapsed time(ex: 1hr, ~1hr, 1h20m)')
        return parser

    @staticmethod
    def _add_subparser_cancel(subparsers):
        parser = subparsers.add_parser(name='cancel', help='cancel timetracking')
        return parser

    def _add_subparser_time(self, subparsers):
        parser = subparsers.add_parser(name='time',
            help='Report elapsed time',
            formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-u', '--unit', choices=['hours'], default=None,
            help='Report the elapsed time in hours')
        parser.add_argument('-i', '--input', metavar='file.csv',
            default=self.fcsv,
            help='Specify an input csv file')
        return parser

    def _add_subparser_report(self, subparsers):
        parser = subparsers.add_parser(name='report',
            help='Generate an report for all time units and include cumulative time',
            formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-i', '--input', metavar='file.csv', nargs='*',
            #default=self.fcsv,
            help='Specify an input csv file')
        parser.add_argument('-o', '--output', metavar='file.docx',
            help='Specify an output file')
        parser.add_argument('-p', '--product', type=float,
            help=SUPPRESS)  # Future feature
        return parser

    def _add_subparser_csv(self, subparsers):
        parser = subparsers.add_parser(name='csv',
            help='Show the locations of csv files managed by timetracker',
            formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-g', '--global', action='store_true',
            help='Look for csv files for all projects tracked in the global config file')
        return parser

    def _add_subparser_csvupdate(self, subparsers):
        parser = subparsers.add_parser(name='csvupdate',
            help='Update values in csv columns containing weekday, am/pm, and duration',
            formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-f', '--force', action='store_true',
            help='Over-write the csv indicated in the project `config` by `filename`')
        parser.add_argument('-i', '--input', metavar='file.csv',
            default=self.fcsv,
            help='Specify an input csv file')
        parser.add_argument('-o', '--output', metavar='file.csv',
            default='updated.csv',
            help='Specify an output csv file')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
