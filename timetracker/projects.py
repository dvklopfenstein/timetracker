"""Manage projects"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

#from os import remove
#from os.path import exists
#from os.path import basename
#from os.path import join
#from os.path import abspath
#from os.path import dirname
#from os.path import normpath
#from datetime import datetime
#from datetime import timedelta
#from logging import debug
from collections import namedtuple

from timetracker.cfg.doc_local import get_docproj
#from timetracker.utils import orange
#from timetracker.utils import prt_todo
#from timetracker.consts import DIRTRK
#from timetracker.consts import FMTDT
#from timetracker.consts import FMTDT_H
#from timetracker.cfg.utils import get_username
#from timetracker.msgs import str_tostart_epoch
#from timetracker.msgs import str_how_to_stop_now
#from timetracker.msgs import str_started_epoch
#from timetracker.msgs import str_not_running
#from timetracker.msgs import str_no_time_recorded
#from timetracker.epoch.epoch import str_arg_epoch

# command   | Needs CfgGlobal
#-----------|----------------
# cancel    |
# common    |
# csvupdate |
# start     |
# stop      |
# none      |
# hours     | G
# init      | G
# projects  | G
# report    | G
# csvloc    | G

from timetracker.cfg.doc_local import DocProj


NTO = namedtuple('NtCsv', 'fcsv project username')

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
    return NTO(fcsv=fcsv, project=project, username=username)

def _get_nt_username(doc, fcfgproj, username, dirhome):
    """For username, get nt w/fcsv & project -- get fcsv and project from CfgProj"""
    assert username is not None
    docproj = DocProj(doc, fcfgproj)
    fcsv = docproj.get_filename_csv(username, dirhome)
    return NTO(fcsv=fcsv, project=doc.get('project'), username=username)

#def _get_nt_all(doc, fcfgproj, dirhome):
#    """For all usernames, get nt w/fcsv & project -- get fcsv and project from CfgProj"""
#    docproj = DocProj(doc, fcfgproj)
#    fcsvs = docproj.get_filenames_csv(dirhome)
#    return NTO(fcsv=fcsv, project=doc.get('project'), username=username)

def _str_err(err, filenamecfg):
    return f'Note: {err.args[1]}: {filenamecfg}'


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
