"""Command line interface (CLI) for timetracking"""
# https://stackoverflow.com/questions/42703908/how-do-i-use-importlib-lazyloader
# https://python.plainenglish.io/lazy-imports-the-secret-to-faster-python-code-c33ae9eb1b13

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"


from timetracker.cmd.init      import cli_run_init
from timetracker.cmd.start     import cli_run_start
from timetracker.cmd.stop      import cli_run_stop
from timetracker.cmd.projects  import cli_run_projects
from timetracker.cmd.cancel    import cli_run_cancel
from timetracker.cmd.hours     import cli_run_hours
from timetracker.cmd.csv       import cli_run_csv
from timetracker.cmd.report    import cli_run_report
from timetracker.cmd.invoice    import cli_run_invoice
from timetracker.cmd.paid       import cli_run_paid
#from timetracker.cmd.tag       import cli_run_tag
from timetracker.cmd.activity  import cli_run_activity
#from timetracker.cmd.csvloc   import cli_run_csvloc


FNCS = {
    'init'     : cli_run_init,
    'start'    : cli_run_start,
    'stop'     : cli_run_stop,
    'cancel'   : cli_run_cancel,
    'hours'    : cli_run_hours,
    'csv'      : cli_run_csv,
    'report'   : cli_run_report,
    'invoice'  : cli_run_invoice,
    'paid'     : cli_run_paid,
    #'tag'      : cli_run_tag,
    'activity' : cli_run_activity,
    'projects' : cli_run_projects,
    #'csvloc'   : cli_run_csvloc,
}


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
