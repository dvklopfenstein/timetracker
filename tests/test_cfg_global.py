#!/usr/bin/env python3
"""Test the TimeTracker global configuration"""

from os.path import join
from os.path import dirname
from os.path import expanduser
from subprocess import run
from logging import debug
from logging import DEBUG
from logging import basicConfig
from tempfile import TemporaryDirectory
from timetracker.cfg.cfg_global import CfgGlobal
from timetracker.cfg.cfg_local import CfgProj
from timetracker.cfg.utils import get_relpath_adj
from tests.pkgtttest.mkprojs import mkdirs
from tests.pkgtttest.mkprojs import findhome

basicConfig(level=DEBUG)

SEP = f'{"-"*80}\n'

def test_cfgbase_home():
    """Test instantiating a default CfgGlobal"""
    cfg = CfgGlobal()
    assert cfg.fname == join(expanduser('~'), '.timetrackerconfig')
    assert cfg.doc['projects'] == []
    #system(f'cat {cfg.fname}')

def test_cfgbase_temp(name='tester', trksubdir='.timetracker'):
    """Test cfg flow"""
    print(f'{SEP}1) INITIALIZE "HOME" DIRECTORY')
    with TemporaryDirectory() as tmp_home:
        cfgtop = get_cfgglobal_empty(tmp_home)
        _run(f'cat {cfgtop.fname}')
        print(f'{SEP}2) Create local project directories')
        proj2wdir = mkdirs(tmp_home)
        findhome(tmp_home)
        print(f'{SEP}3) Create a local cfg object for the apples project')
        exp_projs = []
        for proj, projdir in proj2wdir.items():
            print(f'{SEP}ADD PROJECT({proj}): {projdir}')
            workdir = join(projdir, trksubdir)
            # cfgname_proj = /tmp/tmptrz29mh6/proj/apples/.timetracker/config
            cfgname_proj = join(workdir, 'config')
            # EXP: apples '~/proj/apples/.timetracker/config'
            exp_projs.append([proj, get_relpath_adj(cfgname_proj, tmp_home)])
            # INIT LOCAL PROJECT CONFIG
            cfgloc = CfgProj(cfgname_proj, project=proj, name=name)
            assert cfgloc.trksubdir == trksubdir, (f'\nEXP({trksubdir})\n'
                                                   f'ACT({cfgloc.trksubdir})\n'
                                                   f'{cfgloc}')
            assert cfgloc.dircfg == workdir
            assert cfgloc.project == proj
            assert cfgloc.name == name
            cfgloc.mk_dircfg()
            cfgloc.wr_cfg_new()
            # cat project/.timetracker/config
            fnamecfg_proj = cfgloc.get_filename_cfglocal()
            debug(f'PROJ CFG: {fnamecfg_proj}')
            _run(f'cat {fnamecfg_proj}')
            # ADD PROJECT TO GLOBAL CONFIG AND WRITE
            cfgtop.add_proj(proj, fnamecfg_proj)
            assert cfgtop.doc["projects"].unwrap() == exp_projs, (
                'UNEXPECTED PROJS:\n'
                f'EXP({exp_projs})\n'
                f'ACT({cfgtop.doc["projects"].unwrap()})')
            cfgtop.wr_cfg()
            _run(f'cat {cfgtop.fname}')
            findhome(workdir)


def get_cfgglobal_empty(tmp_home, wrcfg=True):
    """Get an empty Global Configuration file"""
    cfgtop = CfgGlobal(tmp_home)
    assert cfgtop.fname == join(tmp_home, '.timetrackerconfig'), f'{cfgtop.fname}'
    assert cfgtop.doc['projects'] == []
    if wrcfg:
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
    cfg = CfgGlobal()
    assert dirname(cfg.fname) == expanduser('~')

    with TemporaryDirectory() as tmp_home:
        cfg = CfgGlobal(dirhome=tmp_home.name)
        assert dirname(cfg.fname) == tmp_home.name
        tmp_home.cleanup()

def _run(cmd):
    debug(run(cmd.split(), capture_output=True, text=True, check=True).stdout)


if __name__ == '__main__':
    #test_dirhome()
    #test_cfgbase_home()
    test_cfgbase_temp()
