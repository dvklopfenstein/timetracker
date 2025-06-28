"""Command line interface (CLI) for timetracking"""
# https://stackoverflow.com/questions/42703908/how-do-i-use-importlib-lazyloader
# https://python.plainenglish.io/lazy-imports-the-secret-to-faster-python-code-c33ae9eb1b13

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"


# pylint: disable=import-outside-toplevel
def _cli_run_init(fcfgloc, args):
    from timetracker.cmd.init      import cli_run_init
    return cli_run_init(fcfgloc, args)

def _cli_run_start(fcfgloc, args):
    from timetracker.cmd.start     import cli_run_start
    return cli_run_start(fcfgloc, args)

def _cli_run_stop(fcfgloc, args):
    from timetracker.cmd.stop      import cli_run_stop
    return cli_run_stop(fcfgloc, args)

def _cli_run_projects(fcfgloc, args):
    from timetracker.cmd.projects  import cli_run_projects
    return cli_run_projects(fcfgloc, args)

def _cli_run_running(fcfgloc, args):
    from timetracker.cmd.running  import cli_run_running
    return cli_run_running(fcfgloc, args)

def _cli_run_cancel(fcfgloc, args):
    from timetracker.cmd.cancel    import cli_run_cancel
    return cli_run_cancel(fcfgloc, args)

def _cli_run_hours(fcfgloc, args):
    from timetracker.cmd.hours     import cli_run_hours
    return cli_run_hours(fcfgloc, args)

def _cli_run_csv(fcfgloc, args):
    from timetracker.cmd.csv       import cli_run_csv
    return cli_run_csv(fcfgloc, args)

def _cli_run_report(fcfgloc, args):
    from timetracker.cmd.report    import cli_run_report
    return cli_run_report(fcfgloc, args)

def _cli_run_invoice(fcfgloc, args):
    from timetracker.cmd.invoice    import cli_run_invoice
    return cli_run_invoice(fcfgloc, args)

def _cli_run_paid(fcfgloc, args):
    from timetracker.cmd.paid       import cli_run_paid
    return cli_run_paid(fcfgloc, args)

def _cli_run_activity(fcfgloc, args):
    from timetracker.cmd.activity  import cli_run_activity
    return cli_run_activity(fcfgloc, args)

#from timetracker.cmd.start     import cli_run_start
#from timetracker.cmd.stop      import cli_run_stop
#from timetracker.cmd.projects  import cli_run_projects
#from timetracker.cmd.cancel    import cli_run_cancel
#from timetracker.cmd.hours     import cli_run_hours
#from timetracker.cmd.csv       import cli_run_csv
#from timetracker.cmd.report    import cli_run_report
#from timetracker.cmd.invoice    import cli_run_invoice
#from timetracker.cmd.paid       import cli_run_paid
##from timetracker.cmd.tag       import cli_run_tag
#from timetracker.cmd.activity  import cli_run_activity
##from timetracker.cmd.csvloc   import cli_run_csvloc


FNCS = {
    'init'     : _cli_run_init,
    'start'    : _cli_run_start,
    'stop'     : _cli_run_stop,
    'cancel'   : _cli_run_cancel,
    'hours'    : _cli_run_hours,
    'csv'      : _cli_run_csv,
    'report'   : _cli_run_report,
    'invoice'  : _cli_run_invoice,
    'paid'     : _cli_run_paid,
    #'tag'      : _cli_run_tag,
    'activity' : _cli_run_activity,
    'projects' : _cli_run_projects,
    'running' : _cli_run_running,
    #'csvloc'   : _cli_run_csvloc,
}


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
