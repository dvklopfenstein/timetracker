#!/usr/bin/env python3
"""Test the TimeTracker global configuration"""

from os import remove
from os.path import join
from os.path import exists
from logging import DEBUG
from logging import basicConfig
from tempfile import TemporaryDirectory
from timetracker.cfg.cfg import Cfg
#from timetracker.cfg.utils import run_cmd
from tests.pkgtttest.consts import SEP2 as SEP
from tests.pkgtttest.mkprojs import mk_projdirs
from tests.pkgtttest.mkprojs import findhome

basicConfig(level=DEBUG)


def test_cfg_init_force(project='bread', trksubdir='.timetracker'):
    """Test cfg flow"""
    print(f'{SEP}1) INITIALIZE "HOME" DIRECTORY')
    with TemporaryDirectory() as tmphome:
        gfname = join(tmphome, '.acfg')

        print(f'{SEP}2) Create local project directories')
        ntdirs = _makedirs(tmphome, project)

        print(f'{SEP}3) Initialize the {project} project')
        cfg = Cfg(ntdirs.cfglocfilename, gfname, tmphome)
        assert cfg.cfg_glb.filename == gfname
        _init_proj(cfg, project, ntdirs, tmphome, trksubdir)

        print(f'{SEP}4) rm global config, {cfg.cfg_glb.filename}')
        _rm_cfgs(cfg, loc=False, glb=True, tmphome=tmphome)

        print(f'{SEP}5) reinitialize {project} project')
        cfg.reinit(project)
        #    # cat project/.timetracker/config
        #    filenamecfg_proj = cfg.cfg_loc.get_filename_cfg()
        #    debug(f'PROJ CFG: {filenamecfg_proj}')
        #    #debug(run_cmd(f'cat {filenamecfg_proj}'))
        #    # ADD PROJECT TO GLOBAL CONFIG AND WRITE
        #    doc_glo = cfg_glo.add_project(proj, filenamecfg_proj)
        #    assert doc_glo["projects"].unwrap() == exp_projs, (
        #        'UNEXPECTED PROJS:\n'
        #        f'EXP({exp_projs})\n'
        #        f'ACT({doc_glo["projects"].unwrap()})')
        #    ####cfg_glo.wr_cfg()
        #    debug(run_cmd(f'cat {cfg_glo.filename}'))
        #    findhome(trkdir)

def _makedirs(tmphome, project):
    ntdirs = mk_projdirs(tmphome, project)
    print(ntdirs)
    findhome(tmphome)
    return ntdirs

def _init_proj(cfg, project, ntdirs, tmphome, trksubdir):
    # cfgname_proj = /tmp/tmptrz29mh6/proj/apples/.timetracker/config
    # EXP: apples '~/proj/apples/.timetracker/config'
    # INIT LOCAL PROJECT CONFIG
    assert cfg.cfg_loc.trksubdir == trksubdir, (
        f'\nEXP({trksubdir})\n'
        f'ACT({cfg.cfg_loc.trksubdir})\n'
        f'{cfg.cfg_loc}')
    assert cfg.cfg_loc.dircfg == ntdirs.dirtrk
    cfg.init(project)
    assert exists(cfg.cfg_glb.filename)
    assert exists(cfg.cfg_loc.filename)
    findhome(tmphome)

def _rm_cfgs(cfg, loc, glb, tmphome):
    if loc:
        assert exists(cfg.cfg_loc.filename)
        remove(cfg.cfg_loc.filename)
        assert not exists(cfg.cfg_loc.filename)
    if glb:
        assert exists(cfg.cfg_glb.filename)
        remove(cfg.cfg_glb.filename)
        assert not exists(cfg.cfg_glb.filename)
    findhome(tmphome)

if __name__ == '__main__':
    test_cfg_init_force()
