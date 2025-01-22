"""Initialize a timetracker project"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import makedirs
from os.path import exists
from os.path import abspath


def run_init(fmgr):
    """Initialize timetracking on a project"""
    dirtrk = fmgr.get_workdir()
    if not exists(dirtrk):
        makedirs(dirtrk, exist_ok=True)
        absdir = abspath(dirtrk)
        print(f'Initialized empty timetracker directory: {absdir} '
              f'for name({fmgr.name})')
        ##fout_cfg = join(absdir, 'config')
        ##with open(fout_cfg, 'w', encoding='utf8') as ostrm:
        ##    print('', file=ostrm)


##class CmdInit:
##    """Initialize a timetracker project"""
##    # pylint: disable=too-few-public-methods
##
##    def __init__(self, cfgfile):
##        self.cfgfile = cfgfile


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
