"""Command line interface (CLI) for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import argv
from sys import exit as sys_exit
from os import getcwd
#from os.path import normpath
#from os.path import relpath
from logging import debug


from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from argparse import SUPPRESS
from timetracker import __version__
from timetracker.cfg.utils import get_username
from timetracker.cfg.finder import CfgFinder

from timetracker.cmd.none      import cli_run_none
from timetracker.cmd.init      import cli_run_init
from timetracker.cmd.start     import cli_run_start
from timetracker.cmd.stop      import cli_run_stop
from timetracker.cmd.cancel    import cli_run_cancel
from timetracker.cmd.time      import cli_run_time
#from timetracker.cmd.csvloc    import cli_run_csvloc
#from timetracker.cmd.csvupdate import cli_run_csvupdate


def main():
    """Connect all parts of the timetracker"""
    #from logging import basicConfig, DEBUG
    #basicConfig(level=DEBUG)
    obj = Cli()
    obj.run()

fncs = {
    'init'     : cli_run_init,
    'start'    : cli_run_start,
    'stop'     : cli_run_stop,
    'cancel'   : cli_run_cancel,
    'time'     : cli_run_time,
    #'csvloc'   : cli_run_csvloc,
    #'csvupdate': cli_run_csvupdate,
}

class Cli:
    """Command line interface (CLI) for timetracking"""

    ARGV_TESTS = {
        'trksubdir': set(['--trksubdir']),
    }

    def __init__(self, args=None):
        self.finder = CfgFinder(getcwd(), self._init_trksubdir())
        self.parser = self.init_parser_top('timetracker')
        ####self.args = self._init_args_cli() if args is None else self._init_args_test(args)
        self.args = self._init_args(args)

    def run(self):
        """Run timetracker"""
        filename_cfgproj = self.finder.get_cfgfilename()
        debug(f'Cli RUNNNNNNNNNNNNNNNNNN ARGS: {self.args}')
        debug(f'Cli RUNNNNNNNNNNNNNNNNNN DIRTRK:  {self.finder.get_dirtrk()}')
        debug(f'Cli RUNNNNNNNNNNNNNNNNNN CFGNAME: {filename_cfgproj}')
        if self.args.command is not None:
            fncs[self.args.command](filename_cfgproj, self.args)
        else:
            cli_run_none(filename_cfgproj, self.args)

    def _init_args(self, arglist):
        """Get arguments for ScriptFrame"""
        args = self.parser.parse_args(arglist)
        self._adjust_args(args)
        debug(f'TIMETRACKER ARGS: {args}')
        if args.version:
            print(f'trk {__version__}')
            sys_exit(0)
        return args

    def _init_trksubdir(self):
        found = False
        for arg in argv:
            if found:
                debug(f'Cli FOUND: argv --trksubdir {arg}')
                return arg
            if arg == '--trksubdir':
                found = True
        return None


    def _adjust_args(self, args):
        """Replace config default values with researcher-specified values"""
        debug(f'ARGV: {argv}')
        #argv_set = set(argv)
        # If a test set a proj dir other than ./timetracker, use it
        ####if not argv_set.isdisjoint(self.ARGV_TESTS['trksubdir']):
        ####    print('XXXXXXXXXXXXXXXXXXX', self.finder.trksubdir)
        ####    print('XXXXXXXXXXXXXXXXXXX', args.trksubdir)
        return args

    def _get_dflt_csvdir(self):
        """Get the default csv file directory to display in the help message"""
        return self.finder.get_dircsv_default()

    def _get_dflt_csvfilename(self):
        """Get the default csv filename to display in the help message"""
        return 'file.csv'
        ##return self.finder.dirproj

    # -------------------------------------------------------------------------------
    ####def _init_parsers(self):
    ####    parser = self._init_parser_top()
    ####    self._add_subparsers(parser)
    ####    return parser

    def init_parser_top(self, progname):
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
        parser.add_argument('-n', '--username', metavar='NAME', dest='name', default=get_username(),
            help="A person's alias or username for timetracking")
        parser.add_argument('-q', '--quiet', action='store_true',
            help='Only print error and warning messages; information will be suppressed.')
        parser.add_argument('--version', action='store_true',
            help='Print the timetracker version')
        self._add_subparsers(parser)
        return parser

    def _add_subparsers(self, parser):
        subparsers = parser.add_subparsers(dest='command', help='timetracker subcommand help')
        self._add_subparser_init(subparsers)
        self._add_subparser_start(subparsers)
        #self._add_subparser_restart(subparsers)
        self._add_subparser_stop(subparsers)
        self._add_subparser_cancel(subparsers)
        self._add_subparser_time(subparsers)
        #self._add_subparser_csvupdate(subparsers)
        ##self._add_subparser_files(subparsers)
        ##return parser

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
            formatter_class=ArgumentDefaultsHelpFormatter)
        # DEFAULTS: dir_csv project
        parser.add_argument('--csvdir', default=self._get_dflt_csvdir(),
            help='Directory for csv files storing start and stop times')
        parser.add_argument('-p', '--project', default=self.finder.project,
            help="The name of the project to be time tracked")
        return parser

    @staticmethod
    def _add_subparser_start(subparsers):
        parser = subparsers.add_parser(name='start', help='start timetracking')
        # test feature: force over-writing of start time
        parser.add_argument('-@', '--at', metavar='time',
            help='start tracking at a specific or elapsed time')
        parser.add_argument('-f', '--force', action='store_true',
            help='Force restart timer now or `--at` a specific or elapsed time')
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
        parser.add_argument('-@', '--at', metavar='time',
            help='Start tracking at a specific or elapsed time')
        return parser

    @staticmethod
    def _add_subparser_cancel(subparsers):
        parser = subparsers.add_parser(name='cancel', help='cancel timetracking')
        return parser

    @staticmethod
    def _add_subparser_time(subparsers):
        parser = subparsers.add_parser(name='time', help='Report elapsed time')
        parser.add_argument('-u', '--unit', choices=['hours'], default=None,
            help='Report the elapsed time in hours')
        return parser

    def _add_subparser_csvupdate(self, subparsers):
        parser = subparsers.add_parser(name='csvupdate',
            help='Update values in csv columns containing weekday, am/pm, and duration',
            formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-f', '--force', action='store_true',
            help='Over-write the csv indicated in the project `config` by `filename`')
        parser.add_argument('-i', '--input', metavar='file.csv',
            default=self._get_dflt_csvfilename(),
            help='Specify an input csv file')
        parser.add_argument('-o', '--output', metavar='file.csv',
            default='updated.csv',
            help='Specify an output csv file')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
