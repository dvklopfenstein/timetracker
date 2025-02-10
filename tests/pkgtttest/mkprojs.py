"""Create projects in a given temporary directory"""

from os import makedirs
from os.path import join
from os.path import exists
from subprocess import run
from logging import debug
from collections import namedtuple

from timetracker.consts import DIRTRK
from timetracker.cmd.init import run_init_test

RELCSVS = [
    "filename.csv",
    "./filename.csv",
    "../filename.csv",
    "~/filename.csv",
]

def mkdirs(tmp_home):
    """Make sub-directories in a temporary directory for use in tests"""
    projs = {
        'apples'      : join(tmp_home, 'proj/apples'),
        'blueberries' : join(tmp_home, 'proj/blueberries'),
        'cacao'       : join(tmp_home, 'proj/cacao'),
    }
    for pdir in projs.values():
        dirdoc = join(pdir, 'doc')
        makedirs(dirdoc)
    return projs

def mk_projdirs(tmphome, project='apples', dirgit=False):
    """Make sub-directories in a temporary directory for use in tests"""
    pdir = join(tmphome, f'proj/{project}')
    makedirs(join(pdir, 'doc'))
    if dirgit:
        makedirs(join(pdir, '.git'))
    return _get_expdirs(tmphome, project, dirgit)

def _get_expdirs(tmphome, project='apples', dirgit=False, trksubdir=None):
    """Make a list of expected home, project, and git directories"""
    nto = namedtuple("ExpDirs", "dirhome dirproj dirgit dirdoc cfglocfilename")
    dirproj = join(tmphome, 'proj', project)
    if trksubdir is None:
        trksubdir = DIRTRK
    ntexpdirs = nto(
        dirhome=tmphome,
        dirproj=dirproj,
        cfglocfilename=join(dirproj, trksubdir, 'config'),
        dirgit=join(dirproj, '.git') if dirgit else None,
        dirdoc=join(dirproj, 'doc'))
    for key, expdir in ntexpdirs._asdict().items():
        print(f'exists({int(exists(expdir)) if expdir is not None else "."}) '
              f'{key:14} {expdir}')
    return ntexpdirs


def mk_projdirs_wcfgs(tmp_home, project, trksubdir='.timetracker'):
    """Make sub-directories & cfgs in a temporary directory for use in tests"""
    ##dirproj = mk_projdirs(tmp_home, project)
    ntexpdirs = mk_projdirs(tmp_home, project)
    fname_cfgproj = join(ntexpdirs.dirproj, trksubdir, 'config')
    cfgproj, cfg_global = run_init_test(fname_cfgproj, '.', project, tmp_home)
    return ntexpdirs.dirproj, cfgproj, cfg_global


def findhome(home):
    """Do a find on the given homedir"""
    cmd = f'find {home}'
    debug(f'COMMAND: {cmd}\n'
          f'{run(cmd.split(), capture_output=True, text=True, check=True).stdout}')
