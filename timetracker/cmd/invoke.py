"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import exit as sys_exit
from os.path import exists
#from os.path import abspath
#from os.path import relpath
from os.path import dirname
from logging import debug

##from timeit import default_timer
#from timetracker.msgs import str_timed
#from timetracker.msgs import str_notrkrepo
from timetracker.msgs import str_init
from timetracker.utils import yellow
from timetracker.cfg.cfg_local  import CfgProj
from timetracker.csvold import CsvFile
from timetracker.docx import GenWordDoc


def cli_run_invoke(fnamecfg, args):
    """Initialize timetracking on a project"""
    if exists(args.input):
        run_io(args.input, args.output)
        return
    run_invoke(
        fnamecfg,
        args.name,
        perhour=args.perhour,
        fin=args.input,
        fout=args.output,
    )

def run_invoke(fnamecfg, uname, **kwargs):
    """Initialize timetracking on a project"""
    debug(yellow('START: RUNNING COMMAND INVOICE'))
    if not exists(fnamecfg):
        print(str_init(dirname(fnamecfg)))
        sys_exit(0)
    cfgproj = CfgProj(fnamecfg, dirhome=kwargs.get('dirhome'))
    fcsv = cfgproj.get_filename_csv(uname)
    if not exists(fcsv):
        _no_csv(fcsv, cfgproj, uname)
        return None
    return run_io(fcsv, None)

def run_io(fcsv, fout_docx):
    """Run input output"""
    ocsv = CsvFile(fcsv)
    data = ocsv.get_data()
    for d in data:
        print(d)
    if data and fout_docx:
        doc = GenWordDoc(data)
        doc.write_doc(fout_docx)


def _no_csv(fcsv, cfgproj, uname):
    print(f'CSV file does not exist: {fcsv}')
    start_obj = cfgproj.get_starttime_obj(uname)
    start_obj.prtmsg_started01()


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
