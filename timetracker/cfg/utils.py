"""Utilities for configuration parser"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import environ
from os.path import isdir
from os.path import isabs
from os.path import exists
from os.path import expanduser
from os.path import relpath
from os.path import abspath
from os.path import normpath
#from os.path import split
#from os.path import ismount
#from os.path import dirname
from os.path import join
##from os.path import commonpath
from os.path import commonprefix
from subprocess import run
from logging import debug
from logging import warning

def get_abspath(fnam, dirproj, dirhome=None):
    """Get the path of the path fnam relative to dirproj"""
    if isabs(fnam):
        return normpath(fnam)
    if fnam == '':
        return dirproj
    if fnam[:1] == '~':
        fnam = expanduser(fnam) if dirhome is None else abspath(fnam.replace('~', dirhome))
    return normpath(join(dirproj, fnam))

def get_relpath(absfilename, dirproj, dirhome=None):
    """From a absolute path path, get a path relative to the timetracker proj"""
    assert isabs(absfilename)
    assert isabs(dirproj)
    if dirhome is not None:
        isabs(dirhome)
    absfilename = normpath(absfilename)
    if has_homedir(absfilename, dirproj):
        #debug('HAS_PROJDIR')
        return relpath(absfilename, dirproj)
    rpth = relpath(absfilename, dirproj)
    diruser = expanduser('~') if dirhome is None else dirhome
    if has_homedir(absfilename, diruser):
        hpth = f'~/{absfilename[len(diruser)+1:]}'
        #debug(f'EXAMINE HOMEDIR: {absfilename} {diruser} {hpth}')
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
    return run(cmd.split(), capture_output=True, text=True, check=True).stdout

def get_relpath_adj(projdir, dirhome):
    """Collapse an absolute pathname into one with a `~` if projdir is a child of home"""
    if has_homedir(projdir, abspath(dirhome)):
        return join('~', relpath(projdir, dirhome))
    return projdir

def has_homedir(projdir, homedir):
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

def replace_envvar(fpat, username):
    """Replace '$USER$' with the value of the envvar-works with any envvar"""
    pta = fpat.find('$')
    assert pta != -1, f'PATTERN{fpat} USERNAME({username})'
    pt1 = pta + 1
    ptb = fpat.find('$', pt1)
    envkey = fpat[pt1:ptb]
    envval = username if envkey == 'USER' else environ.get(envkey)
    ##debug(f'CFG FNAME: {fpat}')
    ##debug(f'CFG {pta}')
    ##debug(f'CFG {ptb}')
    ##debug(f'CFG ENV:   {envkey} = {envval}')
    return fpat[:pta] + envval + fpat[ptb+1:]

def get_filename_abs(fname):
    """Get the absolute filename"""
    return abspath(expanduser(fname))

def chk_isdir(dname, prefix=''):
    """Check that a file or directory exists"""
    debug(f'{prefix}: INFO exists({int(exists(dname))}) {dname}')
    debug(f'{prefix}: INFO  isdir({int(isdir(dname))}) {dname}')
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
    debug(f'replace_homepath UPDATE FNAME: {fname}')
    debug(f'replace_homepath UPDATE HOME:  {home_str}')
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

def get_dirhome_globalcfg(dirhome=None):
    """Get the home directory, where the global configuration will be stored"""
    assert not dirhome
    return expanduser('~') if 'TIMETRACKERCONF' not in environ else environ['TIMETRACKERCONF']


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
