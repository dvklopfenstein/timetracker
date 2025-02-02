"""Functions to find the local project config, if one exists"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

#from os import environ
#from os import getcwd
from os.path import exists
from os.path import abspath
from os.path import dirname
from os.path import join
from os.path import ismount
#from os.path import basename
#
#
#def get_username(name=None):
#    """Get the default username"""
#    if name is None:
#        return environ.get('USER', 'researcher')
#    if name in environ:
#        return environ[name]
#    return name

def get_project(project=None):
    """Get the default project name"""
    return basename(getcwd()) if project is None else project

def get_abspathtrk(path, trksubdir):
    """Get .timetracker/ proj dir by searching up parent path"""
    trkabsdir, found = finddirtrk(path, trksubdir)
    return trkabsdir if found else None

def finddirtrk(path, trksubdir):
    """Walk up dirs until find .timetracker/ proj dir or mount dir"""
    path = abspath(path)
    trkdir = join(path, trksubdir)
    if exists(trkdir):
        return trkdir, True
    while not ismount(path):
        trkdir = join(path, trksubdir)
        if exists(trkdir):
            return trkdir, True
        path = dirname(path)
    return path, False


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
