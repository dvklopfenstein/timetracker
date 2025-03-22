#!/usr/bin/env python3
"""Test the TimeTracker global configuration"""

from os.path import join
from os.path import exists
from os.path import expanduser
from logging import debug
from logging import DEBUG
from logging import basicConfig
from tempfile import TemporaryDirectory
from timetracker.consts import FILENAME_GLOBALCFG
from timetracker.cfg.cfg_global import CfgGlobal
from timetracker.cfg.cfg_local import CfgProj
#from timetracker.cfg.utils import get_relpath_adj
from timetracker.cfg.utils import run_cmd
from tests.pkgtttest.mkprojs import mkdirs
from tests.pkgtttest.mkprojs import findhome

basicConfig(level=DEBUG)

SEP = f'{"-"*80}\n'

def test_cfgbase_home():
    """Test instantiating a default CfgGlobal"""
    with TemporaryDirectory() as tmphome:
        cfg = CfgGlobal(join(tmphome, FILENAME_GLOBALCFG))
        assert cfg.filename == join(tmphome, '.timetrackerconfig')
        assert cfg.doc['projects'] == []
        assert not exists(cfg.filename)

def test_cfgbase_temp(trksubdir='.timetracker'):
    """Test cfg flow"""
    print(f'{SEP}1) INITIALIZE "HOME" DIRECTORY')
    with TemporaryDirectory() as tmphome:
        cfgtop = _get_cfgglobal_empty(tmphome)
        debug(run_cmd(f'cat {cfgtop.filename}'))
        print(f'{SEP}2) Create local project directories')
        proj2wdir = mkdirs(tmphome)
        findhome(tmphome)
        print(f'{SEP}3) Create a local cfg object for the apples project')
        exp_projs = []
        for proj, projdir in proj2wdir.items():
            print(f'{SEP}ADD PROJECT({proj}): {projdir}')
            workdir = join(projdir, trksubdir)
            # cfgname_proj = /tmp/tmptrz29mh6/proj/apples/.timetracker/config
            cfgname_proj = join(workdir, 'config')
            # EXP: apples '~/proj/apples/.timetracker/config'
            exp_projs.append([proj, cfgname_proj])
            # INIT LOCAL PROJECT CONFIG
            #cfgloc = CfgProj(cfgname_proj, project=proj)
            cfgloc = CfgProj(cfgname_proj)
            assert cfgloc.trksubdir == trksubdir, (f'\nEXP({trksubdir})\n'
                                                   f'ACT({cfgloc.trksubdir})\n'
                                                   f'{cfgloc}')
            assert cfgloc.dircfg == workdir
            assert cfgloc.project == proj
            cfgloc.write_file()
            # cat project/.timetracker/config
            filenamecfg_proj = cfgloc.get_filename_cfg()
            debug(f'PROJ CFG: {filenamecfg_proj}')
            #debug(run_cmd(f'cat {filenamecfg_proj}'))
            # ADD PROJECT TO GLOBAL CONFIG AND WRITE
            cfgtop.add_proj(proj, filenamecfg_proj)
            assert cfgtop.doc["projects"].unwrap() == exp_projs, (
                'UNEXPECTED PROJS:\n'
                f'EXP({exp_projs})\n'
                f'ACT({cfgtop.doc["projects"].unwrap()})')
            cfgtop.wr_cfg()
            debug(run_cmd(f'cat {cfgtop.filename}'))
            findhome(workdir)


def _get_cfgglobal_empty(tmphome):
    """Write and get an empty Global Configuration file/object"""
    cfgtop = CfgGlobal(join(tmphome, FILENAME_GLOBALCFG))
    assert cfgtop.filename == join(tmphome, '.timetrackerconfig'), f'{cfgtop.filename}'
    doc = cfgtop.rd_cfg()
    assert doc is None
    assert cfgtop.doc['projects'] == []
    cfgtop.wr_cfg()
    doc = cfgtop.rd_cfg()
    assert doc is not None
    # pylint: disable=unsubscriptable-object
    assert doc['projects'] == cfgtop.doc['projects']
    #debug(f"XXXXX {doc['projects']}")
    #debug(f"YYYYY {cfgtop.doc['projects']}")
    assert doc['projects'] == cfgtop.doc['projects']
    return cfgtop

def test_dirhome():
    """Test the TimeTracker global configuration"""
    fcfg = join(expanduser('~'), FILENAME_GLOBALCFG)
    cfg = CfgGlobal(fcfg)
    assert cfg.filename == fcfg, f'{cfg.filename} != {fcfg}'

    with TemporaryDirectory() as tmphome:
        fcfg = join(tmphome, FILENAME_GLOBALCFG)
        cfg = CfgGlobal(fcfg)
        assert cfg.filename == fcfg


if __name__ == '__main__':
    test_cfgbase_home()
    test_cfgbase_temp()
    test_dirhome()
