"""Get timetracker data formatted for a report"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from collections import namedtuple
from timetracker.consts import FMTDT12HM
from timetracker.timecalc import timedelta_to_hms


NTTIMEDATA = namedtuple('TimeData', 'start_datetime duration message activity tags')

def get_data_formatted(timedata):
    """Get timetracker data formatted for a report"""
    has_activity, has_tags = _has_activity_tags(timedata)
    nto = _get_nto(has_activity, has_tags)
    return FUNCS[(has_activity, has_tags)](nto, timedata)

# ---------------------------------------------------------------------
def _has_activity_tags(timedata):
    has_activity = False
    has_tags = False
    for ntd in timedata:
        if not has_activity and ntd.activity != '':
            has_activity = True
        if not has_tags and ntd.tags != '':
            has_tags = True
        if has_activity and has_tags:
            break
    return has_activity, has_tags

def _get_nto(has_activity, has_tags):
    flds = _get_nto_fieldnames(has_activity, has_tags)
    return namedtuple('TimeText', flds)

def _get_nto_fieldnames(has_activity, has_tags):
    lst = ['Weekday', 'Starttime', 'Duration']
    if has_activity:
        lst.append('Activity')
    lst.append('Description')
    if has_tags:
        lst.append('Tags')
    return lst

def _nttxt(ntd):
    weekday = ntd.start_datetime.strftime('%a')
    startdt = ntd.start_datetime.strftime(FMTDT12HM)
    hours, minutes, _ = timedelta_to_hms(ntd.duration)
    return (weekday, startdt, f'{hours:02}:{minutes:02}')

def _get_dfmttd_at00(nto, nts):
    # pylint: disable=protected-access
    return [nto._make(_nttxt(e) + (e.message,)) for e in nts]

def _get_dfmttd_at10(nto, nts):
    # pylint: disable=protected-access
    return [nto._make(_nttxt(e) + (e.activity, e.message)) for e in nts]

def _get_dfmttd_at01(nto, nts):
    # pylint: disable=protected-access
    return [nto._make(_nttxt(e) + (e.message, e.tags)) for e in nts]

def _get_dfmttd_at11(nto, nts):
    # pylint: disable=protected-access
    return [nto._make(_nttxt(e) + (e.activity, e.message, e.tags)) for e in nts]

FUNCS = {
    (False, False): _get_dfmttd_at00,
    (False, True) : _get_dfmttd_at01,
    ( True, False): _get_dfmttd_at10,
    ( True, True) : _get_dfmttd_at11,
}


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
