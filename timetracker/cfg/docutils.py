"""Utilities for configuration parser"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved'
__author__ = "DV Klopfenstein, PhD"

from collections import namedtuple
from tomlkit.exceptions import NonExistentKey
from tomlkit.exceptions import ParseError


NTKEYVAL = namedtuple('RdKey', 'value error')


def get_value(doc, key, key2=None):
    """Read a global or project config file only if it exists and is readable"""
    error = None
    try:
        value = doc[key]
        if key2 is not None:
            value = value[key2]
    except (TypeError,NonExistentKey,ParseError) as err:
        error = err
        #print(f'{type(err).__name__}{err.args}')
    else:
        return NTKEYVAL(value=value, error=error)
    return NTKEYVAL(value=None, error=error)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
