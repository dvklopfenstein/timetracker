"""Checks for Finder values"""

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
