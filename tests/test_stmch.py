#!/usr/bin/env python3
"""Test state machines used for finding datetime in free text"""

from timeit import default_timer
from datetime import timedelta
from timetracker.utils import white
from tests.pkgtttest.stmach import _SmAmPm
from tests.pkgtttest.stmach import _SDD
from tests.pkgtttest.stmach import _HH


def test_ampm():
    """Test state machines used for finding 'am', 'pm', 'AM', or 'PM' in free text"""
    _run_ampm(txt='5pm',          exp=['pm'])
    _run_ampm(txt='5pm 3am',      exp=['pm', 'am'])
    _run_ampm(txt='5pm a 3am a ', exp=['pm', 'am'])
    _run_ampm(txt='5pm xtra txt', exp=['pm'])
    _run_ampm(txt='ampm',         exp=['am', 'pm'])
    _run_ampm(txt='13:23:00',     exp=[])

def test_sdd():
    r"""Test state machines used for finding ':\d\d' in free text"""
    _run_sdd(txt='5pm',           exp=[])
    _run_sdd(txt='13:23:00',      exp=[':23', ':00'])
    _run_sdd(txt='13 :23 :00 :a', exp=[':23', ':00'])

def test_hour():
    r"""Test state machines used for finding ':\d\d' in free text"""
    _run_hour(txt='12',      exp=['12'])
    _run_hour(txt='1',       exp=[])  # Needs to be followed by any of: \d : a p A P


# ------------------------------------------------------------------------
def _run_ampm(txt, exp):
    print(white(f'\nTRY TEXT({txt})'))
    tic = default_timer()
    act = _search_for_ampm(txt)
    print(white(f'{timedelta(seconds=default_timer()-tic)} RESULT({act})'))
    assert act == exp, f'TXT({txt})\nTXT({txt}) -> EXP({exp})\nTXT({txt}) -> ACT({act})'

def _search_for_ampm(txt):
    """Examine all letters of the text for AM/PM and semicolon count"""
    smo = _SmAmPm()
    do_search = True
    captures = []
    for letter_cur in txt:
        if do_search:
            do_search = smo.run(letter_cur)
            # Restart state machine
            if smo.state == 'matched':
                captures.append(smo.capture)
                smo.state = 'start'
                do_search = True
    print('_SmAmPm:\n'
        f'  capture={smo.capture}\n'
        f'  captures={captures}\n'
        f'  state={smo.state}')
    return captures

# ------------------------------------------------------------------------
def _run_sdd(txt, exp):
    print(white(f'\nTRY TEXT({txt})'))
    tic = default_timer()
    act = _search_for_sdd(txt)
    print(white(f'{timedelta(seconds=default_timer()-tic)} RESULT({act})'))
    assert act == exp, f'TXT({txt})\nTXT({txt}) -> EXP({exp})\nTXT({txt}) -> ACT({act})'

def _search_for_sdd(txt):
    """Examine all letters of the text for AM/PM and semicolon count"""
    smo = _SDD()
    do_search = True
    captures = []
    for letter_cur in txt:
        if do_search:
            do_search = smo.run(letter_cur)
            # Restart state machine
            if smo.state == 'matched':
                captures.append(smo.capture)
                smo.state = 'start'
                do_search = True
    print('_SDD:\n'
        f'  capture={smo.capture}\n'
        f'  captures={captures}\n'
        f'  state={smo.state}')
    return captures

# ------------------------------------------------------------------------
def _run_hour(txt, exp):
    print(white(f'\nTRY TEXT({txt})'))
    tic = default_timer()
    act = _search_for_hour(txt)
    print(white(f'{timedelta(seconds=default_timer()-tic)} RESULT({act})'))
    assert act == exp, f'TXT({txt})\nTXT({txt}) -> EXP({exp})\nTXT({txt}) -> ACT({act})'

def _search_for_hour(txt):
    """Examine all letters of the text for AM/PM and semicolon count"""
    smo = _HH()
    do_search = True
    captures = []
    for letter_cur in txt:
        if do_search:
            do_search = smo.run(letter_cur)
            # Restart state machine
            if smo.found:
                captures.append(''.join(smo.capture))
                smo.state = 'start'
                do_search = True
    print('_HH:\n'
        f'  capture={smo.capture}\n'
        f'  captures={captures}\n'
        f'  state={smo.state}')
    return captures


if __name__ == '__main__':
    tic_all = default_timer()
    test_ampm()
    test_sdd()
    test_hour()
    print(white(f'{timedelta(seconds=default_timer()-tic_all)} TOTAL TIME FOR ALL TESTS'))
