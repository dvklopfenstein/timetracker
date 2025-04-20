"""Utilities for configuration parser"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved'
__author__ = "DV Klopfenstein, PhD"

from tomlkit import load
from timetracker.utils import prt_err


def read_config(filename, geterrfnc=None):
    """Read a global or project config file only if it exists and is readable"""
    try:
        fptr = open(filename, encoding='utf8')
    except (FileNotFoundError, PermissionError, OSError) as err:
        if geterrfnc:
            print(geterrfnc(err, filename))
        else:
            prt_err(err)
        #print(f'{type(err).__name__}{err.args}')
    else:
        with fptr:
            return load(fptr)
    return None


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
