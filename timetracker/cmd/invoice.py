"""Generate an invoice"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from collections import namedtuple
from datetime import timedelta
from timetracker.cfg.cfg_local import CfgProj
from timetracker.cfg.doc_local import get_docproj
from timetracker.cmd.common import no_csv
from timetracker.cmd.common import str_uninitialized
from timetracker.epoch.calc import str_td
from timetracker.csvfile import CsvFile
from timetracker.docx import WordDoc

NtPaid = namedtuple('NtPaid', 'span cum_time due desc')

def cli_run_invoice(fcfgproj, args):
    """Generate an invoice"""
    if args.fcsv is not None:
        run_invoice_csv(args.fcsv)
        return
    cfgproj = CfgProj(fcfgproj)
    run_invoice_cli(cfgproj, args.name, args.docx, args.hourly_rate)
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
    raise NotImplementedError("OPEN AN ISSUE AT "
        "https://github.com/dvklopfenstein/timetracker/issues/new?template=feature_request.yaml")

def run_invoice_cli(cfgproj, username, fout_docx=None, hourly_rate=100, dirhome=None):
    """Generate an invoice"""
    if not str_uninitialized(cfgproj.filename) and (docproj := get_docproj(cfgproj.filename)):
        fcsv = docproj.get_filename_csv(username, dirhome)
        # pylint: disable=duplicate-code
        ntcsv = run_invoice(fcsv, fout_docx, hourly_rate) if fcsv is not None else None
        if ntcsv.results is None:
            no_csv(fcsv, cfgproj, username)
        return ntcsv
    return None

def run_invoice(fcsv, fout_docx='invoice.docx', hourly_rate=100):  #, report_all=False):
    """Generate an invoice"""
    ##chk_n_convert(fcsv)
    ocsv = CsvFile(fcsv)
    if (ntcsv := CsvFile(fcsv).get_ntdata()) and ntcsv.results:
        num_all = len(ntcsv.results)
        print(f'READ:  {num_all} time units from {ocsv.fcsv}')
        billable = _get_billable_timeslots(ntcsv.results, hourly_rate)
        num_billable = len(billable)
        if num_billable != 0:
            doc = WordDoc()
            ##doc.write_doc(fout_docx)
            doc.write_invoice(fout_docx, billable)
            print(f'WROTE: {num_billable} billable rows of {num_all} total rows: {fout_docx}')
        else:
            print('Use `--bill-all` to get an invoice for all timeslots')
    return ntcsv

def _get_billable_timeslots(nts, hourly_rate, currency_sym='$'):
    ntbillable = [] ##['Day', 'Date', 'HH:SS', 'Total', 'Due', 'Description']
    nto = namedtuple('NtInvoice', 'Day Date Span Total Due Description')
    cum_time = timedelta()
    cum_due = 0.0
    for ntd in sorted(nts, key=lambda nt: nt.start_datetime):
        if ntd.tags != '' and (tags := _get_tags_invoice(ntd.tags)):
            cum_time += ntd.duration
            cum_due = _get_cum_due(cum_due, ntd, tags, hourly_rate)
            ##price = hourly_rate/3600*cum_time.total_seconds()
            ##str_span, str_total str_price = _get_span_n_total(ntd.duration, cum_time, tags)
            ntiv = _get_invoice_row(ntd, cum_time, cum_due, tags, currency_sym)
            ##print('NNNNNNNNNNNNNNNNNNNNN', ntiv)
            nta = nto(
                Day=ntd.start_datetime.strftime('%a'),       # weekday
                Date=ntd.start_datetime.strftime('%Y-%m-%d'), # FMTDT12HM
                Span=ntiv.span,
                Total=ntiv.cum_time,
                Due=ntiv.due,
                Description=ntiv.desc)
            ntbillable.append(nta)
            ##print('AAAAAAAAAAAAAAAAAAAAA', nta)
            ##print(f'BILLABLE: {ntd}')
            ##print(f'BILLABLE: {nta}')
            ##print(f'TAGS: {tags}')
            ##print('')
    return ntbillable

def _get_cum_due(cum_due, ntd, tags, hourly_rate):
    if 'PAID' in tags:
        return cum_due - tags['PAID']
    return cum_due + hourly_rate/3600*ntd.duration.total_seconds()

##def _get_invoice_row(ntd, cum_time, cum_due, tags, hourly_rate, currency_sym):
def _get_invoice_row(ntd, cum_time, cum_due, tags, currency_sym):
    if 'PAID' in tags:
        return NtPaid(
            span='',
            cum_time='',
            ##due=f"{currency_sym}{tags['PAID']:,.0f}",
            ##due=f"{currency_sym}{cum_due:,.0f}",
            due=_str_currency(cum_due, currency_sym),  # , type_paid=True),
            desc=f'PAID {_str_currency(tags["PAID"], currency_sym)}')
    ##return f'{str_td(duration)}', str_td(cum_time)
    ##price = hourly_rate/3600*cum_time.total_seconds()
    return NtPaid(
        span=f'{str_td(ntd.duration)}',
        cum_time=str_td(cum_time),
        ##due=f"{currency_sym}{price:,.0f}",
        ##due=f"{currency_sym}{price:,.0f}",
        due=_str_currency(cum_due, currency_sym),
        desc=ntd.message)

def _get_tags_invoice(strtags):
    """Get tags in an invoice dict"""
    tags = strtags.split(';')
    if 'Billable' not in tags:
        return None
    ret = {}
    for elem in tags:
        if elem == 'Billable':
            ret['Billable'] = True
        if elem[:5] == 'PAID=':
            ret['PAID'] = float(elem[5:])
    return ret

def _str_currency(val, currency_sym):  #, type_paid=False):
    if abs(val) < 1.0:
        return f'{currency_sym}0'  # if not type_paid else ''
    if val > 0:
        return f'{currency_sym}{val:,.0f}'
    return f'-{currency_sym}{val*-1:,.0f}' if abs(val) > 1.0 else f'{currency_sym}{val:,.0f}'



# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
