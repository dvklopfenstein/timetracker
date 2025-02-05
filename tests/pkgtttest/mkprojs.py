"""Create projects in a given temporary directory"""

from os import makedirs
from os.path import join
from subprocess import run
from logging import debug


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

def findhome(home):
    """Do a find on the given homedir"""
    cmd = f'find {home}'
    debug(f'COMMAND: {cmd}\n'
          f'{run(cmd.split(), capture_output=True, text=True, check=True).stdout}')
