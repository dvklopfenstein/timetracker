"""Report all time units"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from logging import debug

from timetracker.cmd.common import get_fcsv
from timetracker.utils import yellow
from timetracker.csvold import CsvFile
from timetracker.docx import WordDoc
from timetracker.timetext import get_data_formatted


def cli_run_report(fnamecfg, args):
    """Report all time units"""
    if args.input is None:
        run_report(fnamecfg, args.name)
    elif len(args.input) == 1:
        run_io(args.input[0], args.output)
    else:
        raise RuntimeError('TIME TO IMPLEMENT')
    ##if args.input and exists(args.input):
    ##    print(args.input)
    ##if args.input and args.output and exists(args.input):
    ##    run_io(args.input, args.output)
    ##    return
    ##run_report(
    ##    fnamecfg,
    ##    args.name,
    ##    fin=args.input,
    ##    fout=args.output,
    ##)

def run_report(fnamecfg, uname, dirhome=None):
    """Report all time units"""
    debug(yellow('RUNNING COMMAND REPORT'))
    fcsv = get_fcsv(fnamecfg, uname, dirhome)
    return run_io(fcsv, None) if fcsv is not None else None

def run_io(fcsv, fout_docx):
    """Run input output"""
    ocsv = CsvFile(fcsv)
    timedata = ocsv.get_data()
    for e in sorted(timedata, key=lambda nt: nt.start_datetime):
        print(e)
    timefmtd = get_data_formatted(timedata)
    if timefmtd:
        for e in timefmtd:
            print(e)
        if fout_docx:
            doc = WordDoc(timefmtd)
            doc.write_doc(fout_docx)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
