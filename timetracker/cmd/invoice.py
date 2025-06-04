"""Generate an invoice"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from timetracker.cfg.cfg_local import CfgProj
from timetracker.cfg.doc_local import get_docproj
from timetracker.cmd.common import no_csv
from timetracker.csvfile import CsvFile
from timetracker.docx import WordDoc
from timetracker.epoch.text import get_data_formatted
from timetracker.csvrun import chk_n_convert
from timetracker.report import prt_basic
from timetracker.msgs import str_init


def cli_run_invoice(fcfgproj, args):
    """Generate an invoice"""
    if args.fcsv is not None:
        run_invoice_csv(args.fcsv)
        return
    cfgproj = CfgProj(fcfgproj)
    run_invoice_cli(cfgproj, args.name, args.docx)
    ##elif len(args.input) == 1:
    ##    _run_io(args.input[0], args.output, pnum=args.product)
    ##else:
    ##    raise RuntimeError('TIME TO IMPLEMENT')
    ##if args.input and exists(args.input):
    ##    print(args.input)
    ##if args.input and args.output and exists(args.input):
    ##    _run_io(args.input, args.output)
    ##    return
    ##run_invoice(
    ##    fnamecfg,
    ##    args.name,
    ##    fin=args.input,
    ##    fout=args.output,
    ##)

def run_invoice_csv(fcsv):
    """Generate an invoice from timeunits in a csv file"""
    raise NotImplementedError("OPEN AN ISSUE AT https://github.com/dvklopfenstein/timetracker/issues/new?template=feature_request.yaml")

def run_invoice_cli(cfgproj, username, fout_docx=None, dirhome=None):
    """Generate an invoice"""
    if (docproj := get_docproj(cfgproj.filename)):
        fcsv = docproj.get_filename_csv(username, dirhome)
        ntcsv = run_invoice(fcsv, fout_docx) if fcsv is not None else None
        if ntcsv.results is None:
            no_csv(fcsv, cfgproj, username)
        return ntcsv
    print(str_init(cfgproj.filename))
    return None

def run_invoice(fcsv, fout_docx):
    """Generate an invoice"""
    chk_n_convert(fcsv)
    ocsv = CsvFile(fcsv)
    ntcsv = ocsv.get_ntdata()
    if ntcsv.results:
        timefmtd = get_data_formatted(ntcsv.results)
        prt_basic(timefmtd)
        if fout_docx:
            doc = WordDoc(timefmtd)
            doc.write_doc(fout_docx)
    return ntcsv


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
