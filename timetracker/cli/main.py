"""Command line interface (CLI) for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

import os
import sys
#from timeit import default_timer  # PRT
#tic = default_timer()             # PRT
#from datetime import timedelta    # PRT
#print(f'{timedelta(seconds=default_timer()-tic)} AFTER IMPORT datetime.timedelta')  # PRT
#print(f'{timedelta(seconds=default_timer()-tic)} BEFORE IMPORT Cli')  # PRT
import timetracker.cli.cli as modcli
#print(f'{timedelta(seconds=default_timer()-tic)} AFTER  IMPORT Cli')  # PRT


def main(username='researcher'):
    """Connect all parts of the timetracker"""
    #from logging import basicConfig, DEBUG
    #basicConfig(level=DEBUG)
    #print('ENTERING Cli')
    args_sys = sys.argv[1:]
    username = os.environ.get('USER', username)
#    print(f'{timedelta(seconds=default_timer()-tic)} AFTER  sys.argv[1:]')  # PRT
    if not args_sys:
        pass
        # pylint: disable=import-outside-toplevel
#        from timetracker.cmd.none import run_none
#        run_none(self.fcfg, username)
#        print('NO ARGS') # PRT
#        ##print(f'{timedelta(seconds=default_timer()-tic)} AFTER  sys.argv[1:]')  # PRT
        # timetracker/cmd/common.py  str_uninitialized
    obj = modcli.Cli(username)
    #print('ENTERING Cli.run')
    obj.run()
    #print('EXITING  Cli.run')


if __name__ == '__main__':
    main()

# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
