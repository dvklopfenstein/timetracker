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
from tomlkit import parse

def parse_cfg(fin, desc=''):
    """Read a config file and load it into a TOML document"""
    # pylint: disable=unused-argument
    cfgtxt = _read_local_cfg(fin)
    ##debug(f'{desc}({cfgtxt})')
    return parse(cfgtxt) if cfgtxt is not None else None

def _read_local_cfg(fin):
    with open(fin, encoding='utf8') as ifstrm:
        return ''.join(ifstrm.readlines())
    return None

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

def chk_isdir(dname, prefix=''):
    """Check that a file or directory exists"""
    debug(f'{prefix}: exists({int(exists(dname))}) {dname}')
    debug(f'{prefix}:  isdir({int(isdir(dname))}) {dname}')
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

def get_cfgdir(cfgdir):
    """Get a global configuration directory which exists"""
    if cfgdir == '~':
        return expanduser(cfgdir)
    if exists(cfgdir):
        return cfgdir
    absdir = abspath(cfgdir)
    if exists(absdir):
        return absdir
    ## pylint: disable=fixme
    ## TODO: Accomodate alternamte directories
    #if absdir[-12:] == '.timetracker':
    #    ret = absdir[:-12]
    #    if exists(ret):
    #        return ret
    if hasattr(environ, cfgdir):
        ret = environ[cfgdir]
        if exists(ret):
            return ret
        raise RuntimeError(f'NO DIRECTORY IN ENVVAR {cfgdir}: {cfgdir}')
    raise RuntimeError(f'UNKNOWN DIRECTORY FOR CONFIGURATION: {cfgdir}')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
