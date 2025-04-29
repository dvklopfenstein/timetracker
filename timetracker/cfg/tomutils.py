"""Utilities for configuration parser"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved'
__author__ = "DV Klopfenstein, PhD"

from collections import namedtuple
from tomlkit import load
from tomlkit import dump


NTRDCFG = namedtuple('RdCfg', 'filename doc error')

def read_config(filename):
    """Read a global or project config file only if it exists and is readable"""
    error = None
    try:
        fptr = open(filename, encoding='utf8')
    except (FileNotFoundError, PermissionError, OSError) as err:
        error = err
        #print(f'{type(err).__name__}{err.args}')
    else:
        with fptr:
            return NTRDCFG(filename=filename, doc=load(fptr), error=error)
    return NTRDCFG(filename=filename, doc=None, error=error)

def write_config(filename, doc, mode='w'):
    """Write a global or project config file"""
    error = None
    try:
        fptr = open(filename, mode, encoding='utf8')
    except (PermissionError, OSError) as err:
        error = err
        #print(f'{type(err).__name__}{err.args}')
    else:
        with fptr:
            dump(doc, fptr)
    return error


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
