"""Create projects in a given temporary directory"""

from os import makedirs
from os.path import exists
from os.path import join
from subprocess import run
from logging import basicConfig
from logging import DEBUG
from logging import debug
from tempfile import TemporaryDirectory
from timetracker.cfg.finder import CfgFinder


def mkdirs(tmp_home):
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
    debug(run(f'find {home}'.split(), capture_output=True, text=True, check=True).stdout)
