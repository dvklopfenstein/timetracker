"""Create projects in a given temporary directory"""

from os import walk
from os import makedirs
from os import environ
from os.path import join
from os.path import exists
from os.path import splitext
from os.path import basename
from subprocess import run
from logging import debug
from collections import namedtuple
from collections import defaultdict
from regex import compile as re_compile

from timetracker.consts import DIRTRK

RELCSVS = [
    "filename.csv",
    "./filename.csv",
    "../filename.csv",
    "~/filename.csv",
    #"~user/filename.csv",
]

CMPPROJ = re_compile(r'^.*/proj/([^/]+)/')


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


def getmkdirs_filename(tmproot, dirname, filename):
    """Get an absolute filename, make dirs if necessary"""
    sharedir = join(tmproot, dirname)
    makedirs(sharedir)
    return join(sharedir, filename)

def reset_env(envvarname, origval, expcurval):
    """Reset an environmental variable to its original value"""
    if origval is None and envvarname in environ:
        del environ[envvarname]
        return
    assert exists(expcurval), expcurval
    assert environ[envvarname] == expcurval
    if origval:
        environ[envvarname] = origval
    else:
        environ.pop(envvarname)
    assert environ.get(envvarname) is None

def mk_projdirs(tmphome, project='apples', dirgit=False, trksubdir=None):
    """Make sub-directories in a temporary directory for use in tests"""
    if project is None:
        project = 'apples'
    pdir = join(tmphome, f'proj/{project}')
    ddir = join(pdir, 'doc')
    if not exists(ddir):
        makedirs(ddir)
    gdir = join(pdir, '.git')
    if dirgit and not exists(gdir):
        makedirs(gdir)
    if trksubdir is None:
        trksubdir = DIRTRK
    return _get_expdirs(tmphome, project, dirgit, trksubdir)

def _get_expdirs(tmphome, project, dirgit, trksubdir):
    """Make a list of expected home, project, and git directories"""
    nto = namedtuple("ExpDirs",
                     "project trksubdir "
                     "dirhome dirproj dirgit dirtrk dirdoc cfglocfilename")
    dirproj = join(tmphome, 'proj', project)
    if trksubdir is None:
        trksubdir = DIRTRK
    ntexpdirs = nto(
        project=project,
        trksubdir=trksubdir,
        dirhome=tmphome,
        dirproj=dirproj,
        cfglocfilename=join(dirproj, trksubdir, 'config'),
        dirgit=join(dirproj, '.git') if dirgit else None,
        dirtrk=join(dirproj, trksubdir),
        dirdoc=join(dirproj, 'doc'))
    return ntexpdirs

def findhome(home):
    """Do a find on the given homedir and print using debug logging"""
    debug(findhome_str(home))

def findhome_str(home, find_opts=''):
    """Do a find on the given homedir and return results in a string"""
    return run_cmd(f'find {home} {find_opts}')

def run_cmd(cmd, prtcmd=True):
    """Run a command and return the string, with the command repeated"""
    txt = []
    if prtcmd:
        txt.append(f"{'- '*40}\n")
        txt.append(f'COMMAND: {cmd}\n')
    txt.append(f'{run(cmd.split(), capture_output=True, text=True, check=True).stdout}')
    return ''.join(txt)

def get_files(basedir):
    """Get files recursively starting from the basedir"""
    files_all = []
    for root, _, files_cur in walk(basedir):
        for file in files_cur:
            files_all.append(join(root, file))
    return files_all

def prt_files(basedir, prefix=''):
    """Print files in basedir and below"""
    for fname in get_files(basedir):
        print(f'{prefix}{fname}')

def get_type2files(basedir):
    """Recursively walk dirs to get files & group by type (config, csv)"""
    type2files = defaultdict(set)
    files_all = get_files(basedir)
    for file in files_all:
        base, ext = splitext(file)
        if ext:
            type2files[ext].add(file)
        else:
            type2files[basename(base)].add(file)
    return type2files

def prt_type2files(basedir):
    """Print files, grouped by type"""
    for typ, files in get_type2files(basedir).items():
        for fname in files:
            print(f'{typ:6} {fname}')

def get_projectname(path):
    """Get proj from: /tmp/tmpxd751piq/home/david/proj/shepherding/"""
    if (mtch := CMPPROJ.search(path)):
        return mtch.group(1)
    return None
