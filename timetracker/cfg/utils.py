"""Utilities for configuration parser"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import environ
from os.path import isdir
from os.path import exists
from os.path import expanduser
from os.path import abspath
from os.path import normpath
from os.path import dirname
from logging import debug
from logging import warning


def replace_envvar(fpat):
    """Replace '$USER$' with the value of the envvar-works with any envvar"""
    pta = fpat.find('$')
    assert pta != -1
    pt1 = pta + 1
    ptb = fpat.find('$', pt1)
    envkey = fpat[pt1:ptb]
    envval = environ.get(envkey)
    ##debug(f'CFG FNAME: {fpat}')
    ##debug(f'CFG {pta}')
    ##debug(f'CFG {ptb}')
    ##debug(f'CFG ENV:   {envkey} = {envval}')
    return fpat[:pta] + envval + fpat[ptb+1:]

def get_filename_abs(fname):
    """Get the absolute filename"""
    return normpath(abspath(expanduser(fname)))

def get_dirname_abs(fname):
    """Get the absolute directory name"""
    return dirname(get_filename_abs(fname))

def chk_isdir(dname):
    """Check that a file or directory exists"""
    debug(f'CFG DIR: exists({int(exists(dname))}) {dname}')
    debug(f'CFG DIR:  isdir({int(isdir(dname))}) {dname}')
    if isdir(dname):
        return True
    warning(f'Directory does not exist: {dname}')
    return False

def replace_homepath(fname):
    """Replace '~' with the expanded filepath"""
    fname = normpath(fname)
    home_str = expanduser('~')
    home_len = len(home_str)
    debug(f'UPDATE FNAME: {fname}')
    debug(f'UPDATE HOME:  {home_str}')
    return fname if fname[:home_len] != home_str else f'~{fname[home_len:]}'


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
