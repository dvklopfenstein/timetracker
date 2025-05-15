"""Get the csv filename(s) that contain time units"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists as path_exists
from collections import namedtuple
from timetracker.cfg.doc_local import get_docproj


NTCSV = namedtuple('NtCsv', 'fcsv project username')
NTCFG = namedtuple('NtCfg', 'fcfgproj, ntcsv')

def get_csv_local_uname(fcfgproj, username, dirhome=None):
    """Get csvs in the local project config file for a specific user"""
    if (docproj := get_docproj(fcfgproj)):
        return get_csv_proj_uname(docproj, username, dirhome)
    return None

def get_csv_proj_uname(docproj, username, dirhome=None):
    """Get csvs in the local project config file for a specific user"""
    assert username is not None
    fcsv = docproj.get_filename_csv(username, dirhome)
    if path_exists(fcsv):
        return NTCSV(fcsv=fcsv, project=docproj.project, username=username)
    return None

def get_csvs_global_uname(projects, username, dirhome=None):
    """Get csvs in projects listed in a global config file for a specific user"""
    ret = []
    for _, fcfgproj in projects:
        if (ntcsv := get_csv_local_uname(fcfgproj, username, dirhome)) is not None:
            ret.append(NTCFG(fcfgproj=fcfgproj, ntcsv=ntcsv))
    return ret

#def get_csvs_local_all(fcfgproj, dirhome=None):
#    """Get csvs in the local project config file for a all users"""
#    if (docproj := get_docproj(fcfgproj)):
#        return _get_nts_all(docproj, username, dirhome)
#    return None
#
#def get_csvs_global_all(fcfgproj, dirhome=None):
#    """Get csvs in projects listed in a global config file for a all users"""
#    assert fcfgproj
#    assert dirhome
#
#def _get_nt_all(docproj, dirhome):
#    """For username, get nt w/fcsv & project -- get fcsv and project from CfgProj"""
#    fcsv = docproj.get_filenames_csv(dirhome)
#    return NTCSV(exists=path_exists(fcsv), fcsv=fcsv, project=docproj.project, username=username)

####def _get_nt_username(docproj, username, dirhome):
####    """For username, get nt w/fcsv & project -- get fcsv and project from CfgProj"""
####    assert username is not None
####    fcsv = docproj.get_filename_csv(username, dirhome)
####    if path_exists(fcsv):
####        return NTCSV(exists=path_exists(fcsv),
####                     fcsv=fcsv,
####                     project=docproj.project,
####                     username=username)


####def get_csvs_username(projects, username, dirhome=None):
####    """Get csvs for the given projects for a single username"""
####    assert username is not None
####    ret = []
####    for _, fcfgproj in projects:
####        ntcfg = read_config(fcfgproj)
####        if ntcfg.doc:
####            if (ntd := _get_nt_username(ntcfg.doc, fcfgproj, username, dirhome)):
####                ret.append(ntd)
####    return ret
####
#####def get_csvs_all(projects, dirhome=None):
#####    """Get csvs for the given projects for a single username"""
#####    ret = []
#####    for _, fcfgproj in projects:
#####        ntcfg = read_config(fcfgproj)
#####        doc = ntcfg.doc
#####        if doc:
#####            if (ntd := _get_nt_all(doc, fcfgproj, dirhome)):
#####                ret.append(ntd)
#####    return ret

def get_ntcsvproj01(fcfgproj, fcsv, username):
    """Get nt w/fcsv & project -- get project from CfgProj and fcsv from param"""
    project = None
    if (docproj := get_docproj(fcfgproj)):
        project = docproj.project
    return NTCSV(fcsv=fcsv, project=project, username=username)

##def _get_nt_username(doc, fcfgproj, username, dirhome):
##    """For username, get nt w/fcsv & project -- get fcsv and project from CfgProj"""
##    assert username is not None
##    docproj = DocProj(doc, fcfgproj)
##    fcsv = docproj.get_filename_csv(username, dirhome)
##    return NTCSV(fcsv=fcsv, project=doc.get('project'), username=username)

#def _get_nt_all(doc, fcfgproj, dirhome):
#    """For all usernames, get nt w/fcsv & project -- get fcsv and project from CfgProj"""
#    docproj = DocProj(doc, fcfgproj)
#    fcsvs = docproj.get_filenames_csv(dirhome)
#    return NTCSV(fcsv=fcsv, project=doc.get('project'), username=username)

##def _str_err(err, filenamecfg):
##    return f'Note: {err.args[1]}: {filenamecfg}'


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
