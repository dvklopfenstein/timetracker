#!/usr/bin/env python3
"""Test the TimeTracker global configuration"""

from os import remove
from os.path import join
from os.path import exists
from logging import DEBUG
from logging import basicConfig
from tempfile import TemporaryDirectory
from timetracker.cfg.cfg import Cfg
from tests.pkgtttest.consts import SEP1
from tests.pkgtttest.consts import SEP2
from tests.pkgtttest.consts import SEP3
from tests.pkgtttest.mkprojs import mk_projdirs
from tests.pkgtttest.mkprojs import findhome

basicConfig(level=DEBUG)


def test_cfg_init_force(project='bread', trksubdir='.timetracker', fcfg_glo='.acfg'):
    """Test cfg flow"""
    print(f'{SEP2}1) INITIALIZE "HOME" DIRECTORY')
    with TemporaryDirectory() as tmphome:
        gfname = join(tmphome, fcfg_glo)
        run = Run(tmphome, gfname)

        print(f'{SEP2}2) Create local project directories')
        ntdirs = mk_projdirs(tmphome, project)
        findhome(tmphome)

        print(f'{SEP2}3) Initialize the {project} project')
        cfg = Cfg(ntdirs.cfglocfilename)  # , gfname, tmphome)
        cfg.init(project, fcfg_global=gfname, dirhome=tmphome)
        run.chk_init_proj(cfg, ntdirs, trksubdir, gfname)
        findhome(tmphome)

        # --------------------------------------------------------
        print(f'{SEP1}4) rm config: global & local')
        run.rm_cfgs(cfg, loc=True, glb=True)
        run.prtcfgs(cfg)

        print(f'{SEP3}5) reinitialize {project} project')
        cfg.reinit(project, fcfg_global=gfname, dirhome=tmphome)
        run.prtcfgs(cfg)
        run.chk_cfg(cfg, loc=True, glb=True)

        # --------------------------------------------------------
        print(f'\n{SEP1}6) rm config: global only')
        run.rm_cfgs(cfg, loc=False, glb=True)
        run.prtcfgs(cfg)

        print(f'{SEP3}7) reinitialize {project} project')
        cfg.reinit(project, fcfg_global=gfname, dirhome=tmphome)
        run.prtcfgs(cfg)
        run.chk_cfg(cfg, loc=True, glb=True)

        # --------------------------------------------------------
        print(f'\n{SEP1}4) rm config: local only')
        run.rm_cfgs(cfg, loc=True, glb=False)
        run.prtcfgs(cfg)

        print(f'{SEP3}5) reinitialize {project} project')
        cfg.reinit(project, fcfg_global=gfname, dirhome=tmphome)
        run.prtcfgs(cfg)
        run.chk_cfg(cfg, loc=True, glb=True)

        # --------------------------------------------------------
        print(f'\n{SEP1}6) rm config: keep all')
        #run.rm_cfgs(cfg, loc=False, glb=False)
        run.prtcfgs(cfg)

        print(f'{SEP3}7) reinitialize {project} project')
        cfg.reinit(project, fcfg_global=gfname, dirhome=tmphome)
        run.prtcfgs(cfg)
        run.chk_cfg(cfg, loc=True, glb=True)

        #    # cat project/.timetracker/config
        #    filenamecfg_proj = cfg.cfg_loc.get_filename_cfg()
        #    debug(f'PROJ CFG: {filenamecfg_proj}')
        #    #debug(run_cmd(f'cat {filenamecfg_proj}'))
        #    # ADD PROJECT TO GLOBAL CONFIG AND WRITE
        #    doc_glo = cfg_glo.ini_project(proj, filenamecfg_proj)
        #    assert doc_glo["projects"].unwrap() == exp_projs, (
        #        'UNEXPECTED PROJS:\n'
        #        f'EXP({exp_projs})\n'
        #        f'ACT({doc_glo["projects"].unwrap()})')
        #    ####cfg_glo.wr_cfg()
        #    debug(run_cmd(f'cat {cfg_glo.filename}'))
        #    findhome(trkdir)

class Run:
    """Test init --force (reinit)"""

    def __init__(self, tmphome, gfname):
        self.tmphome = tmphome
        self.gfname = gfname
        self.cfg_glb = Cfg.get_cfgglobal(gfname, tmphome)

    def prtcfgs(self, cfg):
        """Print the filenames of the local and global filenames"""
        print(f'exists({int(exists(self.cfg_glb.filename))}) {self.cfg_glb.filename}')
        print(f'exists({int(exists(cfg.cfg_loc.filename))}) {cfg.cfg_loc.filename}')

    def chk_init_proj(self, cfg, ntdirs, trksubdir, gfname):
        """Check if the project was initialized properly"""
        # cfgname_proj = /tmp/tmptrz29mh6/proj/apples/.timetracker/config
        # EXP: apples '~/proj/apples/.timetracker/config'
        # INIT LOCAL PROJECT CONFIG
        assert self.cfg_glb.filename == gfname
        assert cfg.cfg_loc.trksubdir == trksubdir, (
            f'\nEXP({trksubdir})\n'
            f'ACT({cfg.cfg_loc.trksubdir})\n'
            f'{cfg.cfg_loc}')
        assert cfg.cfg_loc.dircfg == ntdirs.dirtrk
        assert exists(self.cfg_glb.filename), f'DOES NOT EXIST({self.cfg_glb.filename})'
        assert exists(cfg.cfg_loc.filename)
        ##findhome(tmphome)

    def chk_cfg(self, cfg, loc, glb):
        """Check the local and global config filename"""
        # Check if local config exists or not
        if loc:
            assert exists(cfg.cfg_loc.filename)
        else:
            assert not exists(cfg.cfg_loc.filename)
        # Check if global config exists or not
        if glb:
            assert exists(self.cfg_glb.filename)
        else:
            assert not exists(self.cfg_glb.filename)

    def rm_cfgs(self, cfg, loc, glb):
        """Remove chose config files"""
        if loc:
            assert exists(cfg.cfg_loc.filename)
            remove(cfg.cfg_loc.filename)
            assert not exists(cfg.cfg_loc.filename)
        if glb:
            assert exists(self.cfg_glb.filename)
            remove(self.cfg_glb.filename)
            assert not exists(self.cfg_glb.filename)


if __name__ == '__main__':
    test_cfg_init_force()
