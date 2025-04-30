#!/usr/bin/env python3
"""Test the TimeTracker global configuration"""

from os.path import join
from os.path import dirname
from logging import DEBUG
from logging import basicConfig
from tempfile import TemporaryDirectory
from timetracker.cfg.utils import get_abspath
from timetracker.cfg.doc_local import get_docproj
from timetracker.cmd.init import run_init
from timetracker.utils import cyan
from tests.pkgtttest.consts import SEP2
from tests.pkgtttest.cmpstr import show_cfgs
from tests.pkgtttest.mkprojs import findhome
from tests.pkgtttest.runfncs import proj_setup
from tests.pkgtttest.runfncs import prt_expdirs

basicConfig(level=DEBUG)


def test_cfg_reinit(project='baking', trksubdir='.chef'):
    """Test cfg flow"""
    print(f'{SEP2}1) INITIALIZE "HOME" DIRECTORY')
    with TemporaryDirectory() as tmpdir:
        dirhome = join(tmpdir, 'home')
        _, _, ntexpdirs = proj_setup(dirhome, project,
            dircur='dirproj', dirgit01=True, trksubdir=trksubdir)
        prt_expdirs(ntexpdirs)


        # --------------------------------------------------------
        print(f'{SEP2}1) Initialize the {project} project using REINIT')
        cfg = run_init(ntexpdirs.cfglocfilename,
                       dircsv=None,
                       project=project,
                       dirhome=dirhome)
        findhome(tmpdir)
        docproj = get_docproj(cfg.cfg_loc.filename)
        print(get_abspath(dirname(docproj.csv_filename), ntexpdirs.dirproj, dirhome))
        print(cfg.cfg_loc.get_filename_csv())
        show_cfgs(cfg)

        # --------------------------------------------------------
        # N: Needs reinit
        # Y: No action required, nothing changed
        chk = Chk(cfg, dirhome)
        chk.needs_reinit('N', dircsv=None, project=None, fcfg_global=None)
        chk.needs_reinit('Y', dircsv=None, project=None, fcfg_global=join(dirhome, 'a.cfg'))
        chk.needs_reinit('Y', dircsv=None, project='eating', fcfg_global=None)
        chk.needs_reinit('N', dircsv=ntexpdirs.dirproj, project=None, fcfg_global=None)
        chk.needs_reinit('Y', dircsv=ntexpdirs.dirhome, project=None, fcfg_global=None)


# pylint: disable=too-few-public-methods
class Chk:
    """Check if cfgs need reinit"""

    def __init__(self, cfg, dirhome):
        self.cfg = cfg
        self.dirhome = dirhome

    def needs_reinit(self, exp, dircsv, project, fcfg_global):
        """Check if cfgs need reinit"""
        res = self.cfg.needs_reinit(dircsv, project, fcfg_global, self.dirhome)
        print(res)
        if exp == 'N':
            assert res is None
            print(cyan('Does NOT need reinit\n'))
        else:
            assert res is not None
            print(cyan('NEEDS reinit\n'))


if __name__ == '__main__':
    test_cfg_reinit()
