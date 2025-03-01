"""Report all time units"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from logging import debug

from timetracker.cmd.base import get_fcsv
from timetracker.utils import yellow
from timetracker.csvold import CsvFile
from timetracker.docx import WordDoc


def cli_run_invoke(fnamecfg, args):
    """Report all time units"""
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
    """Report all time units"""
    debug(yellow('START: RUNNING COMMAND INVOICE'))
    fcsv = get_fcsv(fnamecfg, uname, kwargs.get('dirhome'))
    return run_io(fcsv, None)

def run_io(fcsv, fout_docx):
    """Run input output"""
    ocsv = CsvFile(fcsv)
    timedata = ocsv.get_data()
    for d in timedata:
        print(d)
    if timedata and fout_docx:
        doc = WordDoc(timedata)
        for e in doc.nttext:
            print(e)
        doc.write_doc(fout_docx)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
