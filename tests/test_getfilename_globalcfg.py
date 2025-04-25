#!/usr/bin/env python3
"""Test function, get_filename_globalcfg"""

from os import environ
from os.path import join
from os.path import expanduser
from timetracker.cfg.utils import get_filename_globalcfg
from timetracker.consts import FILENAME_GLOBALCFG
from tests.pkgtttest.mkprojs import reset_env


SEP = f'\n{"="*80}\n'


def test_getfilename_globalcfg():
    """Test function, get_filename_globalcfg"""
    dirhome  = '/usr/home/fisher'
    fcfg_cli = '/usr/share/cli/.timetrackerconfig'
    fcfg_doc = '/usr/share/doc/.timetrackerconfig'
    fcfg_env = '/usr/share/env/.timetrackerconfig'

    orig_fglb = environ.get('TIMETRACKERCONF')

    if 'TIMTRACKERCONF' in environ:
        del environ['TIMETRACKERCONF']
    _run_env01(dirhome, fcfg_cli, fcfg_doc)
    _run_env0(dirhome)

    environ['TIMETRACKERCONF'] = fcfg_env
    _run_env01(dirhome, fcfg_cli, fcfg_doc)
    _run_env1(dirhome, fcfg_env)

    reset_env('TIMETRACKERCONF', orig_fglb, fcfg_env)



def _run_env0(dirhome):
    act = get_filename_globalcfg()
    _chk(act, join(expanduser('~'), FILENAME_GLOBALCFG))

    act = get_filename_globalcfg(None,    None,     None)
    _chk(act, join(expanduser('~'), FILENAME_GLOBALCFG))

    act = get_filename_globalcfg(dirhome, None,     None)
    _chk(act, join(dirhome, FILENAME_GLOBALCFG))


def _run_env1(dirhome, fcfg_env):
    act = get_filename_globalcfg()
    _chk(act, fcfg_env)

    act = get_filename_globalcfg(None,    None,     None)
    _chk(act, fcfg_env)

    act = get_filename_globalcfg(dirhome, None,     None)
    _chk(act, fcfg_env)


def _run_env01(dirhome, fcfg_cli, fcfg_doc):
    act = get_filename_globalcfg(None,    None,     fcfg_doc)
    _chk(act, fcfg_doc)

    act = get_filename_globalcfg(None,    fcfg_cli, None)
    _chk(act, fcfg_cli)

    act = get_filename_globalcfg(None,    fcfg_cli, fcfg_doc)
    _chk(act, fcfg_cli)

    act = get_filename_globalcfg(dirhome, None,     fcfg_doc)
    _chk(act, fcfg_doc)

    act = get_filename_globalcfg(dirhome, fcfg_cli, None)
    _chk(act, fcfg_cli)

    act = get_filename_globalcfg(dirhome, fcfg_cli, fcfg_doc)
    _chk(act, fcfg_cli)



def _chk(act, exp):
    assert act == exp, f'ACTUAL != EXPECTED:\nACT({act})\nEXP({exp})'
    print(f'PASSES: {act} == {exp}')


if __name__ == '__main__':
    test_getfilename_globalcfg()
