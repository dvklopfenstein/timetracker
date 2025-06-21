"""Utilities for configuration parser"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import environ
import os.path as op
from os.path import expanduser
from os.path import relpath
from os.path import abspath
from subprocess import run
from timetracker.consts import FILENAME_GLOBALCFG


def get_abspath(fnam, dirproj, dirhome=None):
    """Get the path of the path fnam relative to dirproj"""
    if op.isabs(fnam):
        return op.normpath(fnam)
    if fnam == '':
        return dirproj
    if fnam[:1] == '~':
        fnam = expanduser(fnam) if dirhome is None else abspath(fnam.replace('~', dirhome))
    return op.normpath(op.join(dirproj, fnam))

def get_relpath(absfilename, dirproj, dirhome=None):
    """From a absolute path path, get a path relative to the timetracker proj"""
    assert op.isabs(absfilename)
    assert op.isabs(dirproj)
    if dirhome is not None:
        op.isabs(dirhome)
    absfilename = op.normpath(absfilename)
    if has_homedir(absfilename, dirproj):
        return relpath(absfilename, dirproj)
    rpth = relpath(absfilename, dirproj)
    diruser = expanduser('~') if dirhome is None else dirhome
    if has_homedir(absfilename, diruser):
        hpth = f'~/{absfilename[len(diruser)+1:]}'
        return rpth if len(rpth) < len(hpth) else hpth
    return rpth

def get_username(name=None):
    """Get the default username"""
    if name is None:
        return environ.get('USER', 'researcher')
    if name in environ:
        return environ[name]
    return name

def run_cmd(cmd):
    """Run a command with output to stdout"""
    res = run(cmd.split(), capture_output=True, text=True, check=False)
    return res.stdout if res.returncode == 0 else None

def get_relpath_adj(projdir, dirhome):
    """Collapse an absolute pathname into one with a `~` if projdir is a child of home"""
    if has_homedir(projdir, abspath(dirhome)):
        return op.join('~', relpath(projdir, dirhome))
    return projdir

def has_homedir(projdir, homedir):
    """Checks to see if `projdir` has a root of `rootdir`"""
    assert homedir == abspath(homedir)
    assert projdir == abspath(projdir)
    homedir = abspath(homedir)
    #if commonpath([homedir]) == commonpath([homedir, abspath(projdir)]):
    if homedir == op.commonprefix([homedir, abspath(projdir)]):
        # `projdir` is under `homedir`
        return True
    return False

def replace_envvar(fpat, username):
    """Replace '$USER$' with the value of the envvar-works with any envvar"""
    pta = fpat.find('$')
    assert pta != -1, f'PATTERN{fpat} USERNAME({username})'
    pt1 = pta + 1
    ptb = fpat.find('$', pt1)
    envkey = fpat[pt1:ptb]
    envval = username if envkey == 'USER' else environ.get(envkey)
    return fpat[:pta] + envval + fpat[ptb+1:]

def get_filename_abs(fname):
    """Get the absolute filename"""
    return abspath(expanduser(fname))

def replace_homepath(fname):
    """Replace expanded home dir with '~' if using '~' is shorter"""
    # pylint: disable=fixme
    # TODO: use commonprefix
    #fname = op.normpath(fname)
    fname = abspath(fname)
    home_str = expanduser('~')
    home_len = len(home_str)
    ##debug('replace_homepath UPDATE FNAME: %s', fname)
    ##debug('replace_homepath UPDATE HOME:  %s', home_str)
    return fname if fname[:home_len] != home_str else f'~{fname[home_len:]}'

def get_dirhome(dirhome):
    """Get a global configuration directory which is present"""
    exists = op.exists
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
    frel = op.normpath(relpath(filename))
    return fabs if len(fabs) < len(frel) else frel

def splitall(path):
    """Split a path into all its parts"""
    allparts = []
    while 1:
        parts = op.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        if parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        path = parts[0]
        allparts.insert(0, parts[1])
    return allparts

def get_filename_globalcfg(dirhome=None, fcfg_cli=None, fcfg_doc=None):
    """Get the home directory, where the global configuration will be stored"""
    ####debug('get_filename_globalcfg(\n  dirhome=%2,\n  fcfg_cli=%s,\n  '
    ####      'fcfg_doc=%s,\n  msg=%s)',
    ####      dirhome, fcfg_cli, fcfg_doc, msg)
    # TBD: REMOVE ASSERT
    if fcfg_doc is not None:
        assert '.timetracker' not in splitall(fcfg_doc), \
            f'GLOBAL CONFIG NAME HAS .timetracker {fcfg_doc}'
    if fcfg_cli is None and fcfg_doc is None:  # 00
        if 'TIMETRACKERCONF' not in environ:
            return op.join(expanduser('~') if dirhome is None else dirhome, FILENAME_GLOBALCFG)
        return environ['TIMETRACKERCONF']
    if fcfg_cli is not None:                   # 10 & 11
        return fcfg_cli
    return fcfg_doc                            # 01


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
