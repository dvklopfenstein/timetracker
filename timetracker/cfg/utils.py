"""Utilities for configuration parser"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import environ
from os.path import isdir
from os.path import exists
from os.path import expanduser
from os.path import relpath
from os.path import abspath
from os.path import normpath
from os.path import dirname
from os.path import join
##from os.path import commonpath
from os.path import commonprefix
from logging import debug
from logging import warning

from tomlkit.toml_file import TOMLFile


def parse_cfglocal(fin_cfglocal):
    """Read a config file and load it into a TOML document"""
    doc = TOMLFile(fin_cfglocal).read() if exists(fin_cfglocal) else None
    if doc is not None:
        fpat = abspath(expanduser(doc['csv']['filename']))
        return replace_envvar(fpat) if '$' in fpat else fpat
    return None

####def _read_local_cfg(fin):
####    with open(fin, encoding='utf8') as ifstrm:
####        return ''.join(ifstrm.readlines())
####    return None

def get_relpath_adj(projdir, dirhome):
    """Collapse an absolute pathname into one with a `~` if projdir is a child of home"""
    if has_homedir(abspath(dirhome), projdir):
        return join('~', relpath(projdir, dirhome))
    return projdir

def has_homedir(homedir, projdir):
    """Checks to see if `projdir` has a root of `rootdir`"""
    assert homedir == abspath(homedir)
    assert projdir == abspath(projdir)
    homedir = abspath(homedir)
    ##debug(f'has_homedir      homedir {homedir}')
    ##debug(f'has_homedir      projdir {projdir}')
    #if commonpath([homedir]) == commonpath([homedir, abspath(projdir)]):
    if homedir == commonprefix([homedir, abspath(projdir)]):
        # `projdir` is under `homedir`
        ##debug('has_homedir  has_homedir True')
        return True
    ##debug('has_homedir  has_homedir False')
    return False

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
    return abspath(expanduser(fname))

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
    """Replace expanded home dir with '~' if using '~' is shorter"""
    # pylint: disable=fixme
    # TODO: use commonprefix
    #fname = normpath(fname)
    fname = abspath(fname)
    home_str = expanduser('~')
    home_len = len(home_str)
    debug(f'UPDATE FNAME: {fname}')
    debug(f'UPDATE HOME:  {home_str}')
    return fname if fname[:home_len] != home_str else f'~{fname[home_len:]}'

def get_dirhome(dirhome):
    """Get a global configuration directory which exists"""
    if dirhome == '~':
        return expanduser(dirhome)
    if exists(dirhome):
        return dirhome
    absdir = abspath(dirhome)
    if exists(absdir):
        return absdir
    ## pylint: disable=fixme
    ## TODO: Accomodate alternamte directories
    #if absdir[-12:] == '.timetracker':
    #    ret = absdir[:-12]
    #    if exists(ret):
    #        return ret
    if hasattr(environ, dirhome):
        ret = environ[dirhome]
        if exists(ret):
            return ret
        raise RuntimeError(f'NO DIRECTORY IN ENVVAR {dirhome}: {dirhome}')
    raise RuntimeError(f'UNKNOWN DIRECTORY FOR CONFIGURATION: {dirhome}')

def get_shortest_name(filename):
    """Return the shortest filename"""
    fabs = abspath(filename)
    # pylint: disable=fixme
    # TODO: use commonprefix
    frel = normpath(relpath(filename))
    return fabs if len(fabs) < len(frel) else frel


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
