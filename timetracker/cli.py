"""Command line interface (CLI) for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

#from timeit import default_timer  # PRT
#tic = default_timer()             # PRT
#from datetime import timedelta    # PRT
#print(f'{timedelta(seconds=default_timer()-tic)} TOP OF CLI: IMPORT dt')  # PRT

from sys import argv as sys_argv
from os import getcwd
#from os.path import exists
#from logging import debug
#print(f'{timedelta(seconds=default_timer()-tic)} TOP OF CLI: IMPORT sys, getcwd')  # PRT

from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from argparse import SUPPRESS
#print(f'{timedelta(seconds=default_timer()-tic)} TOP OF CLI: IMPORT argparse')  # PRT
from timetracker.cmd.fncs import FNCS
#print(f'{timedelta(seconds=default_timer()-tic)} TOP OF CLI: IMPORT FNCS')  # PRT
from timetracker.cfg.utils import get_username
from timetracker.cfg.finder import CfgFinder
#print(f'{timedelta(seconds=default_timer()-tic)} TOP OF CLI: AFTER CfgFinder')  # PRT
#from timetracker.cmd.none import cli_run_none
#print(f'{timedelta(seconds=default_timer()-tic)} TOP OF CLI: AFTER cli_run_none')  # PRT

#print(f'{timedelta(seconds=default_timer()-tic)} TOP OF CLI: AFTER IMPORTS')  # PRT

def main():
    """Connect all parts of the timetracker"""
    #from logging import basicConfig, DEBUG
    #basicConfig(level=DEBUG)
    #print('ENTERING Cli')
    obj = Cli()
    #print('ENTERING Cli.run')
    obj.run()
    #print('EXITING  Cli.run')


class Cli:
    """Command line interface (CLI) for timetracking"""
    # pylint: disable=too-few-public-methods

    ARGV_TESTS = {
        'trksubdir': set(['--trk-dir']),
    }

    def __init__(self, args=None):
        sysargs = self._adjust_args(args)
        self.finder = CfgFinder(getcwd(), self._init_trksubdir())
        self.fcfg = self.finder.get_cfgfilename()
        self.user = get_username()  # default username
        self.parser = self._init_parser_top('timetracker')
#        print('PARSE ARGS')                      # PRT
        self.args = self._init_args(sysargs)
#        print(f'TIMETRACKER ARGS: {self.args}')  # PRT

    def run(self):
        """Run timetracker"""
        ##debug('Cli RUNNNNNNNNNNNNNNNNNN ARGS:    %s', self.args)
        ##debug('Cli RUNNNNNNNNNNNNNNNNNN DIRTRK:  %s', self.finder.get_dirtrk())
        ##debug('Cli RUNNNNNNNNNNNNNNNNNN CFGNAME: %s', self.fcfg)
        # pylint: disable=import-outside-toplevel
        if self.args.command is not None:
            FNCS[self.args.command](self.fcfg, self.args)
        else:
            from timetracker.cmd.none import cli_run_none
            cli_run_none(self.fcfg, self.args)

    def _adjust_args(self, given_args):
        """Replace config default values with researcher-specified values"""
        ##debug('ARGV: %s', sys_argv)
        ret = []
        args = sys_argv[1:] if given_args is None else given_args
        optname = None
        for elem in args:
            if optname == '--at':
                #debug(' --at opt was(%s)', elem)
                elem = self._adjust_opt_at(elem)
                #debug(' --at opt now(%s)', elem)
                optname = None
            ret.append(elem)
            if elem == '--at':
                optname = elem
            #debug('ADJUST_ARGS>>(%s)', elem)
        return ret

    @staticmethod
    def _adjust_opt_at(val):
        if val[:1] != '-':
            return val
        return val if val[1:2] == ' ' else ' ' + val

    def _init_args(self, arglist):
        """Get arguments for ScriptFrame"""
        args = self.parser.parse_args(arglist)
        if args.version:
            # pylint: disable=import-outside-toplevel
            from sys import exit as sys_exit
            from timetracker import __version__
            print(f'trk {__version__}')
            sys_exit(0)
        return args

    def _init_trksubdir(self):
        found = False
        for arg in sys_argv:
            if found:
                ##debug('Cli FOUND: argv --trk-dir %s', arg)
                return arg
            if arg == '--trk-dir':
                found = True
        return None

    @staticmethod
    def _get_cmds():
        """In argumentparser, usage=f'%(prog)s [-h] {self._get_cmds()}'"""
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
        parser.add_argument('--trk-dir', metavar='DIR', default=self.finder.trksubdir,
            # Directory that holds the local project config file
            help='Directory that holds the local project config file')
            #help=SUPPRESS)
        parser.add_argument('--username', metavar='NAME', dest='name', default=self.user,
            help="A person's alias or username running a timetracking command")
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
        self._add_subparser_hours(subparsers)
        self._add_subparser_csv(subparsers)
        self._add_subparser_report(subparsers)
        self._add_subparser_invoice(subparsers)
        self._add_subparser_paid(subparsers)
        #self._add_subparser_tag(subparsers)
        #self._add_subparser_activity(subparsers)
        self._add_subparser_projects(subparsers)
        self._add_subparser_running(subparsers)
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
            help='Directory for csv files storing start and stop times')
        parser.add_argument('-f', '--force', action='store_true',
            help='Reinitialize the project: Add missing config files & keep existing')
        parser.add_argument('-p', '--project', default=self.finder.project,
            help="The name of the project to be time tracked")
        parser.add_argument('-G', '--global-config-file', metavar='FILE',
            help='Use specified file as the global config file')
        parser.add_argument('-A', '--no-git-add', action='store_true',
            help='Do not run `git add` on newly created local project timetracker files')
        parser.add_argument( '--dirgit', help=SUPPRESS, default=self.finder.dirgit)
        return parser

    @staticmethod
    def _add_subparser_start(subparsers):
        parser = subparsers.add_parser(name='start', help='start timetracking')
        parser.add_argument('-f', '--force', action='store_true',
            help='Force restart timer now or `--at` a specific or elapsed time')
        parser.add_argument('--at', metavar='time',
            help='start tracking at a '
                 'specific(ex: 4pm, "Tue 4pm") or '
                 'elapsed time(ex: 10min, -10min, 4hr)')
        return parser

    def _add_subparser_stop(self, subparsers):
        parser = subparsers.add_parser(name='stop',
            help='Stop timetracking',
            formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-m', '--message', required=True, metavar='TXT',
            help='Message describing the work done in the time unit')
        parser.add_argument('-k', '--keepstart', action='store_true', default=False,
            #help='Resetting the timer is the normal behavior; Keep the start time this time')
            help=SUPPRESS)
        parser.add_argument('--at', metavar='time',
            help='start tracking at a '
                 'specific(ex: 4pm, "2025-01-05 04:30pm") or '
                 'elapsed time(ex: 1hr, ~1hr, 1h20m)')
        parser.add_argument('-a', '--activity', metavar='txt',
            help='Add an activity to this time slot')
        parser.add_argument('-t', '--tags', nargs='*',
            help='Tags for this time unit')
        parser.add_argument('-b', '--billable', action='store_true',
            help='Tags this time unit as billable')
        return parser

    @staticmethod
    def _add_subparser_cancel(subparsers):
        parser = subparsers.add_parser(name='cancel', help='cancel timetracking')
        return parser

    def _add_subparser_hours(self, subparsers):
        parser = subparsers.add_parser(name='hours',
            help='Report elapsed time in hours',
            formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-i', '--input', metavar='file.csv', nargs='*', dest='fcsv',
            help='Specify an input csv file')
        parser.add_argument('-g', '--global', dest='run_global', action='store_true',
            help=f'List hours for all projects for {self.user}')
        parser.add_argument('-u', '--all-users', dest='all_users', action='store_true',
            help='List hours for all projects for all usernames')
        parser.add_argument('-G', '--global-config-file', metavar='file.cfg',
            help='Use specified file as the global config file')
        return parser

    def _add_subparser_csv(self, subparsers):
        parser = subparsers.add_parser(name='csv',
            help='Get a list of csv files containing timetracking data',
            formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-g', '--global', dest='run_global', action='store_true',
            help='List all csvs for all projects that are listed in the global config file')
        parser.add_argument('--all', action='store_true',
            help='Use specified file as the global config file')
        #parser.add_argument('-G', '--global-config-file', metavar='file.cfg',
        #    help='Use specified file as the global config file')
        return parser

    def _add_subparser_report(self, subparsers):
        parser = subparsers.add_parser(name='report',
            help='Generate a project report for time units and include cumulative time',
            formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('--docx', default='report.docx',
            help='Put report into the named Word document docx file')
        return parser

    def _add_subparser_invoice(self, subparsers):
        parser = subparsers.add_parser(name='invoice',
            help='Generate an invoice',
            formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-i', '--input', metavar='file.csv', dest='fcsv',
            help='Specify an input csv file')
        parser.add_argument('--docx', default='report.docx',
            help='Put report into the named Word document docx file')
        parser.add_argument('-$', '--hourly-rate', type=int, default=100,
            help='Use given hourly rate to calculate charges')
        return parser

    def _add_subparser_paid(self, subparsers):
        parser = subparsers.add_parser(name='paid',
            help='Record the amount paid in the csv file')
        parser.add_argument('amount', type=float,
            help='The amount paid (floating point value)')
        parser.add_argument('--at', metavar='time',
            help='Mark the payment at a '
                 'specific time (ex: 4pm, "2025-01-05 04:30pm")')
        parser.add_argument('-a', '--activity', metavar='txt',
            help='Add an activity to this time slot')
        parser.add_argument('-t', '--tags', nargs='*',
            help='Tags for this time unit')
        return parser

    def _add_subparser_tag(self, subparsers):
        parser = subparsers.add_parser(name='tag',
            help='Show all tags used in this project',
            formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-g', '--run_global', action='store_true',
            help='List all tag for projects found in the global config file')
        parser.add_argument('-G', '--global-config-file', metavar='file.cfg',
            help='Use specified file as the global config file')
        return parser

    def _add_subparser_activity(self, subparsers):
        parser = subparsers.add_parser(name='activity',
            help='Show all activities used in this project')
        parser.add_argument('-g', '--global', dest='run_global', action='store_true',
            help=f'List hours for all projects for {self.user}')
        parser.add_argument('-u', '--all-users', dest='all_users', action='store_true',
            help='List hours for all projects for all usernames')
        parser.add_argument('-G', '--global-config-file', metavar='file.cfg',
            help='Use specified file as the global config file')
        return parser

    def _add_subparser_projects(self, subparsers):
        parser = subparsers.add_parser(name='projects',
            help='Show all projects and the locations of their csv files',
            formatter_class=ArgumentDefaultsHelpFormatter)
        parser.add_argument('-e', '--exists', action='store_true',
            help='Add text indicating if the project exists')
        parser.add_argument('--rm-missing', action='store_true',
            help='Removes projects from the global config that do not exist')
        return parser

    def _add_subparser_running(self, subparsers):
        parser = subparsers.add_parser(name='running',
            help='Show all projects whose timer is running')
        parser.add_argument('-v', '--verbose', action='store_true',
            help='Show project location if the timer is running')
        return parser


if __name__ == '__main__':
    main()

# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
