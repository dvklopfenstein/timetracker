"""Command line interface (CLI) for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from timetracker.cmd.init      import cli_run_init
from timetracker.cmd.start     import cli_run_start
from timetracker.cmd.stop      import cli_run_stop
from timetracker.cmd.csv       import cli_run_csv
from timetracker.cmd.cancel    import cli_run_cancel
from timetracker.cmd.time      import cli_run_time
from timetracker.cmd.report    import cli_run_report
#from timetracker.cmd.csvloc   import cli_run_csvloc
from timetracker.cmd.csvupdate import cli_run_csvupdate


FNCS = {
    'init'     : cli_run_init,
    'start'    : cli_run_start,
    'stop'     : cli_run_stop,
    'cancel'   : cli_run_cancel,
    'time'     : cli_run_time,
    'report'   : cli_run_report,
    'csv'      : cli_run_csv,
    #'csvloc'   : cli_run_csvloc,
    'csvupdate': cli_run_csvupdate,
}


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
