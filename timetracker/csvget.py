"""Utilities for configuration parser"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from collections import namedtuple
from timetracker.cfg.doc_local import get_docproj


NTO = namedtuple('NtCsv', 'fcsv project username')

def get_csvs_local_uname(fcfgproj, username, dirhome=None):
    """Get csvs in the local project config file for a specific user"""
    assert username is not None
    if (docproj := get_docproj(fcfgproj)):
        return _get_nt_username(docproj, username, dirhome)
    return None

def get_csvs_global_uname(projects, username, dirhome=None):
    """Get csvs in projects listed in a global config file for a specific user"""
    # def get_csvs_username(projects, username, dirhome=None):
    assert username is not None
    ret = []
    for _, fcfgproj in projects:
        if (docproj := get_docproj(fcfgproj)):
            if (ntd := _get_nt_username(docproj, username, dirhome)):
                ret.append(ntd)
    return ret

def get_csvs_local_all(cfg, dirhome=None):
    """Get csvs in the local project config file for a all users"""
    assert cfg
    assert dirhome

def get_csvs_global_all(cfg, dirhome=None):
    """Get csvs in projects listed in a global config file for a all users"""
    assert cfg
    assert dirhome

def _get_nt_username(docproj, username, dirhome):
    """For username, get nt w/fcsv & project -- get fcsv and project from CfgProj"""
    assert username is not None
    fcsv = docproj.get_filename_csv(username, dirhome)
    return NTO(fcsv=fcsv, project=docproj.project, username=username)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
