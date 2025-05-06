"""Checks for Finder values"""

from os.path import exists
from os.path import dirname
from os.path import join
from os.path import abspath
from os.path import normpath


def get_filename(filename):
    """Get absolute filename with 'home' as the repo base"""
    return normpath(abspath(join(dirname(__file__), "../..", filename)))

def str_get_dirtrk(dirtrk_exp, finder):
    """Pretty print if assertion fails"""
    dirtrk_act = finder.get_dirtrk()
    return (
        "\n"
        f"EXP: {dirtrk_exp}\n"
        f"ACT: {dirtrk_act}\n"
        f"ACT: {finder}")

def show_cfgs(cfg):
    """Print the contents of both the local project and global config file"""
    show_file(cfg.cfg_loc.filename)
    show_file(cfg.cfg_glb.filename)

def show_file(filename, msg=None):
    """Print the contents of a file"""
    if exists(filename):
        print(f'CONTENTS OF {filename}: --------------------')
        print(str_file(filename, msg))
    else:
        print(f'NOT EXIST   {filename}: --------------------')

def str_file(filename, msg=None):
    """Get a string containing the contents of a file"""
    with open(filename, encoding='utf8') as ifstrm:
        txt = []
        if msg:
            txt.append(f'{msg}\n')
        for line in ifstrm:
            txt.append(line)
        return ''.join(txt)
