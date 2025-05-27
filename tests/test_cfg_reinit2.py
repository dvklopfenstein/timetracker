#!/usr/bin/env python3
"""Test the TimeTracker global configuration"""

from os import mkdir
from os.path import join
from os.path import exists
from collections import namedtuple
from logging import DEBUG
from logging import basicConfig
from tempfile import TemporaryDirectory
from timetracker.consts import FILENAME_GLOBALCFG
from timetracker.cfg.cfg import Cfg
from timetracker.cfg.doc_local import get_docproj
from timetracker.cfg.cfg_global import get_cfgglobal
#from timetracker.cmd.init import run_init
####from timetracker.cmd.init import run_reinit
from tests.pkgtttest.consts import SEP2
#from tests.pkgtttest.consts import SEP3
from tests.pkgtttest.cmpstr import show_file
from tests.pkgtttest.mkprojs import findhome
from tests.pkgtttest.runfncs import proj_setup
from tests.pkgtttest.runfncs import prt_expdirs

basicConfig(level=DEBUG)


def test_cfg_reinit(project='baking', trksubdir='.chef'):
    """Test cfg flow"""
    print(f'{SEP2}0) INITIALIZE "HOME" DIRECTORY')
    with TemporaryDirectory() as tmpdir:
        ntf = _get_filenames(tmpdir)
        dflt_glbcfg = join(ntf.dirhome, FILENAME_GLOBALCFG)
        _, finder, ntexpdirs = proj_setup(ntf.dirhome, project,
            dircur='dirproj', dirgit01=True, trksubdir=trksubdir)
        prt_expdirs(ntexpdirs)
        cfg = Cfg(ntexpdirs.cfglocfilename,
                  get_cfgglobal(
                      fcfg_explicit=dflt_glbcfg,
                      dirhome=ntf.dirhome,
                      fcfg_doc=None))


        # --------------------------------------------------------
        print(f'{SEP2}1) Initialize the {project} project using REINIT')
        assert not exists(dflt_glbcfg)
        cfg.reinit(finder.dirgit,
                   project=project,
                   dircsv=None,
                   dirhome=ntf.dirhome)
        findhome(tmpdir)
        docproj = _chk_cfgs(cfg, exp_docloc_glbcfg=None)
        assert exists(dflt_glbcfg)
        assert docproj.global_config_filename is None
        assert docproj.project == project
        assert docproj.dircsv == '.'

        # --------------------------------------------------------
        print(f'{SEP2}2) reinitialize the {project} project: DIFFERENT GLOBAL CFG({ntf.gfname_a})')
        cfg.reinit(finder.dirgit,
                   project=project,
                   dircsv=None,
                   dirhome=ntf.dirhome,
                   fcfg_global=ntf.gfname_a)  # a.cfg
        findhome(tmpdir)
        docproj = _chk_cfgs(cfg, exp_docloc_glbcfg=ntf.gfname_a)
        assert docproj.global_config_filename == ntf.gfname_a, docproj.global_config_filename
        #run.chk_init_proj(cfg, ntdirs, trksubdir, ntf.gfname_a)

        # --------------------------------------------------------
        print(f'{SEP2}2) reinitialize the {project} project: DIFFERENT GLOBAL CFG({ntf.gfname_a})')
        cfg.reinit(finder.dirgit,
                   project=project,
                   dircsv=None,
                   dirhome=ntf.dirhome,
                   fcfg_global=ntf.gfname_b)
        findhome(tmpdir)
        docproj = _chk_cfgs(cfg, exp_docloc_glbcfg=ntf.gfname_b)
        assert docproj.global_config_filename == ntf.gfname_b, docproj.global_config_filename
        #run.chk_init_proj(cfg, ntdirs, trksubdir, ntf.gfname_a)


def _get_filenames(tmpdir):
    nto = namedtuple('NtFiles', 'dirhome dirshare gfname_dflt gfname_a gfname_b')
    dirshare = join(tmpdir, 'share')
    dirhome = join(tmpdir, 'home')
    mkdir(dirshare)
    return nto(
        dirhome=dirhome,
        dirshare=dirshare,
        gfname_dflt=join(dirhome, FILENAME_GLOBALCFG),
        gfname_a=join(dirshare, 'a.cfg'),
        gfname_b=join(dirshare, 'b.cfg'))

def _chk_cfgs(cfg, exp_docloc_glbcfg):
    show_file(cfg.cfg_loc.filename)
    show_file(cfg.cfg_glb.filename)
    docproj = get_docproj(cfg.cfg_loc.filename)
    assert docproj is not None
    assert docproj.project is not None
    # Check that project is added to list in CfgGlobal
    projects = cfg.cfg_glb.get_projects()
    assert projects
    proj_glb, proj_cfg = projects[-1]
    assert proj_glb == docproj.project
    assert proj_cfg == cfg.cfg_loc.filename
    assert docproj.global_config_filename == exp_docloc_glbcfg, \
        f'docloc["global_config"]["filename"] -- '\
        f'EXP({exp_docloc_glbcfg}) != '\
        f'ACT({docproj.global_config_filename}) '
    if exp_docloc_glbcfg:
        assert exists(exp_docloc_glbcfg), f'DOES NOT EXIST: {exp_docloc_glbcfg}'
    return docproj

        ## --------------------------------------------------------
        #print(f'{sep_test(1)}CFG REINIT TEST 1: rm config: global & local')
        #run.rm_cfgs(cfg, loc=True, glb=True)
        #run.prtcfgs(cfg)

        #print(f'{SEP3}reinitialize {project} project')
        #cfg.reinit(project, fcfg_global=gfname, dirhome=tmphome)
        #run.prtcfgs(cfg)
        #run.chk_cfg(cfg, loc=True, glb=True)

        ## --------------------------------------------------------
        #print(f'\n{sep_test(2)}CFG REINIT TEST 2: rm config: global only')
        #run.rm_cfgs(cfg, loc=False, glb=True)
        #run.prtcfgs(cfg)

        #print(f'{SEP3}reinitialize {project} project')
        #cfg.reinit(project, fcfg_global=gfname, dirhome=tmphome)
        #run.prtcfgs(cfg)
        #run.chk_cfg(cfg, loc=True, glb=True)

        ## --------------------------------------------------------
        #print(f'\n{sep_test(3)}CFG REINIT TEST 3: rm config: local only')
        #run.rm_cfgs(cfg, loc=True, glb=False)
        #run.prtcfgs(cfg)

        #print(f'{SEP3}reinitialize {project} project')
        #cfg.reinit(project, fcfg_global=gfname, dirhome=tmphome)
        #run.prtcfgs(cfg)
        #run.chk_cfg(cfg, loc=True, glb=True)

        ## --------------------------------------------------------
        #print(f'\n{sep_test(4)}CFG REINIT TEST 4: NO rm config: keep all')
        ##run.rm_cfgs(cfg, loc=False, glb=False) # NO rm
        #run.prtcfgs(cfg)

        #print(f'{SEP3}reinitialize {project} project')
        #cfg.reinit(project, fcfg_global=gfname, dirhome=tmphome)
        #run.prtcfgs(cfg)
        #run.chk_cfg(cfg, loc=True, glb=True)

        ## --------------------------------------------------------
        #print(f'\n{sep_test(5)}CFG REINIT TEST 5: NO rm config: keep all & cfg_glb=None')
        ##run.rm_cfgs(cfg, loc=False, glb=False) # NO rm
        #run.prtcfgs(cfg)

        #print(f'{SEP3}reinitialize {project} project')
        #cfg.cfg_glb = None
        #cfg.reinit(project, fcfg_global=gfname, dirhome=tmphome)
        #run.prtcfgs(cfg)
        #run.chk_cfg(cfg, loc=True, glb=True)

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


if __name__ == '__main__':
    test_cfg_reinit()
