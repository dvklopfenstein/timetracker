#!/usr/bin/env python3
"""Test converting free text to datetimes"""

from datetime import timedelta
from timeit import default_timer
from timetracker.utils import white
from timetracker.epoch.stmach import _SmHhSsAm
from timetracker.epoch.stmach import search_texttime
from timetracker.epoch.epoch import _get_dt_ampm
from tests.pkgtttest.timestrs import TIMESTRS


def test_txt_to_dt():
    """Test state machines used for finding 'am', 'pm', 'AM', or 'PM' in free text"""
    for txt, dct in TIMESTRS.items():
        #_run_ampm(txt, dct['exp_dct'])
        act = _get_dt_ampm(txt, None)
        assert act == dct['dt'], ('EXP != ACT:\n'
            f'  TXT: {txt}\n'
            f'  EXP: {dct["dt"]}\n'
            f'  ACT: {act}\n')
        print(f'{act} <- {txt}\n')

def test_txt_to_dct():
    """Test state machines used for finding 'am', 'pm', 'AM', or 'PM' in free text"""
    for txt, dct in TIMESTRS.items():
        #_run_ampm(txt, dct['exp_dct'])
        act = search_texttime(txt)
        assert act == dct['exp_dct'], ('EXP != ACT:\n'
            f'  TXT: {txt}\n'
            f'  EXP: {dct["exp_dct"]}\n'
            f'  ACT: {act}\n')
        print(f'{act} <- {txt}\n')


# ------------------------------------------------------------------------
def _run_ampm(txt, exp):
    print(white(f'\nTRY TXT({txt})'))
    tic = default_timer()
    act = _search_for_ampm(txt)
    print(white(f'{timedelta(seconds=default_timer()-tic)} '
                f'TEXT({txt}) -> RESULT({act})'))
    assert act == exp, f'TXT({txt})\nTXT({txt}) -> EXP({exp})\nTXT({txt}) -> ACT({act})'

def _search_for_ampm(txt):
    """Examine all letters of the text for AM/PM and semicolon count"""
    captures = []
    smo = _SmHhSsAm()
    state = 'start'
    for letter in txt:
        if (state := smo.run(state, letter)) == 'start' and smo.capture:
            captures.append(smo.capture)
            smo.capture = {}
    if (state := smo.run(state, None)) == 'start' and smo.capture:
        captures.append(smo.capture)
    print('CAPTURES:', captures)
    return captures


if __name__ == '__main__':
    tic_all = default_timer()
    test_txt_to_dt()
    test_txt_to_dct()
    print(white(f'{timedelta(seconds=default_timer()-tic_all)} TOTAL TIME FOR ALL TESTS'))
