"""Create projects in a given temporary directory"""

from os import makedirs
from os.path import join
from subprocess import run
from logging import debug

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

def mk_projdirs(tmp_home, project='apples'):
    """Make sub-directories in a temporary directory for use in tests"""
    pdir = join(tmp_home, f'proj/{project}')
    dirdoc = join(pdir, 'doc')
    makedirs(dirdoc)
    return pdir

def mk_projdirs_wcfgs(tmp_home, project, trksubdir='.timetracker'):
    """Make sub-directories & cfgs in a temporary directory for use in tests"""
    dirproj = mk_projdirs(tmp_home, project)
    fname_cfgproj = join(dirproj, trksubdir, 'config')
    cfgproj, cfg_global = run_init_test(fname_cfgproj, '.', project, tmp_home)
    return dirproj, cfgproj, cfg_global


def findhome(home):
    """Do a find on the given homedir"""
    cmd = f'find {home}'
    debug(f'COMMAND: {cmd}\n'
          f'{run(cmd.split(), capture_output=True, text=True, check=True).stdout}')
