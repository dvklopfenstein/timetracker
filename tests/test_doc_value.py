#!/usr/bin/env python3
"""Test getting values of doc items"""

from os.path import join
from os.path import exists
from logging import basicConfig
from tempfile import TemporaryDirectory
from timetracker.cfg.cfg import Cfg
from timetracker.cfg.doc_local import DocProj
from timetracker.cfg.tomutils import read_config
from timetracker.cfg.docutils import get_ntvalue
from timetracker.cmd.init import run_init
from tests.pkgtttest.runfncs import proj_setup
from tests.pkgtttest.mkprojs import findhome_str
from tests.pkgtttest.runfncs import prt_expdirs
from tests.pkgtttest.cmpstr import show_file


SEP = f'\n{"="*80}\n'
SEP2 = f'\n{"- "*20}\n'


def test_doc_value(project='tapistry', username='weaver'):
    """Test getting values of doc items"""
    with TemporaryDirectory() as tmproot:
        basicConfig()
        dirhome = join(tmproot, 'home')
        fcfgproj, finder, expdirs = proj_setup(dirhome, project, dircur='dirproj') # finder
        cfg = Cfg(fcfgproj)
        prt_expdirs(expdirs)

        # Initialize all projects for all usernames
        run_init(cfg, finder.dirgit,
            dircsv=None,
            project=project,
            dirhome=dirhome)
        print(findhome_str(tmproot))  #, '-type f'))
        show_file(cfg.cfg_glb.filename, f'{SEP}GLOBAL CONFIG: {cfg.cfg_glb.filename}')
        show_file(cfg.cfg_loc.filename, f'{SEP}LOCAL CONFIG: {cfg.cfg_loc.filename}')

        print(f'{SEP}LOAD BOTH GLOBAL AND LOCAL CONFIGS')
        ntglb = read_config(cfg.cfg_glb.filename)
        ntloc = read_config(cfg.cfg_loc.filename)

        print(f'{SEP}TEST GETTING ALL PARTS OF ALL CFG FILES')
        assert ntglb.error is None, ntglb.error
        assert ntloc.error is None, ntloc.error
        # Check access to global config items
        print(f'GLOBAL-DOC: {ntglb}')
        _chk_key_good(
            [['tapistry', join(dirhome, 'proj/tapistry/.timetracker/config')]],
            get_ntvalue(ntglb.doc, 'projects'))
        # Check access to local config items
        print(f'LOCAL-DOC:  {ntloc}')
        _chk_key_good(project, get_ntvalue(ntloc.doc, 'project'))
        _chk_key_good(
            f"./timetracker_{project}_$USER$.csv",
            get_ntvalue(ntloc.doc, 'csv', 'filename'))

        print(f'{SEP}TEST BAD ACCESSES TO CFG FILES')
        # Check bad trys to access: NtKey value=None, error=...
        _chk_key_bad(get_ntvalue(ntglb.doc, 'badkey'), "doc['badkey']")
        _chk_key_bad(get_ntvalue(ntloc.doc, 'csv', 'badkey2'), "doc['csv']['badkey']")
        _chk_key_bad(get_ntvalue(ntloc.doc, 'badkey', 'filename'), "doc['badkey']['filename']")
        _chk_key_bad(get_ntvalue(None, 'badkey'), "None['badkey']")
        assert ntloc.doc.get('project') == project
        assert ntloc.doc.get('badkey') is None

        print(f'{SEP}GET CSV FILENAME')
        docprj = DocProj(ntloc.doc, cfg.cfg_loc.filename)
        csvfilename = docprj.get_filename_csv(username)
        assert csvfilename == \
            join(dirhome, 'proj/tapistry/timetracker_tapistry_weaver.csv'), \
            docprj.get_filename_csv(username)
        assert not exists(csvfilename)
        print(f'exists({int(exists(csvfilename))}) {csvfilename}')


def _chk_key_good(val, ntkey):
    assert ntkey.value == val, f'EXP != ACT\nEXP: {val}\nACT: {ntkey.value}'
    assert ntkey.error is None, ntkey

def _chk_key_bad(ntkey, desc):
    assert ntkey.value is None, ntkey
    assert ntkey.error is not None, ntkey
    print(f'DOC ACCESS ERROR: {ntkey.error} GIVEN {desc}')


if __name__ == '__main__':
    test_doc_value()
