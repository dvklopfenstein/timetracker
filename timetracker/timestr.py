"""Local project configuration parser for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from datetime import datetime
from logging import warning
from timetracker.consts import FMTDT
from timetracker.consts import FMTDT24HMS


def get_dt(timestr):
    try:
        return datetime.strptime(timestr, FMTDT)
    except ValueError:
        pass
    try:
        # pylint: disable=fixme
        # TODO: warn to update csv
        return datetime.strptime(timestr, FMTDT24HMS)
    except ValueError as err:
        warning(f'{err}')
        warning(f'UNRECOGNIZED datetime format({timestr})')
        return None


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
