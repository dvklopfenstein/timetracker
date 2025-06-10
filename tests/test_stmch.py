#!/usr/bin/env python3
"""Test state machines used for finding datetime in free text"""

from timeit import default_timer
from datetime import timedelta
from timetracker.utils import white
from timetracker.epoch.stmach import _SmHhSsAm

TESTIO = {
    '5pm':{
        'exp_dct':[{'hour':5, 'AM/PM':'PM'}],
    },

    '5pm 3am':{
        'exp_dct':[{'hour':5, 'AM/PM':'PM'},
                   {'hour':3, 'AM/PM':'AM'}],
    },

    '5pm a 3am a ':{
        'exp_dct':[{'hour':5, 'AM/PM':'PM'},
                   {'hour':3, 'AM/PM':'AM'}],
    },

    '5pm xtra txt':{
        'exp_dct':[{'hour':5, 'AM/PM':'PM'}],
    },

    'ampm':{'exp_dct':[]},

    '13:23:00':{
        'exp_dct':[{'hour':13, 'minute': 23, 'second': 0}],
    },

    '2025':{
        'exp_dct':[{'year': 2025}],
    },

    '2025-06-10 08:57:12 AM':{
        'exp_dct':[{'year': 2025, 'month': 6, 'day': 10},
                   {'hour': 8, 'minute': 57, 'second': 12, 'AM/PM':'AM'}],
    },

    '2025-06-10 8:57:12am':{
        'exp_dct':[{'year': 2025, 'month': 6, 'day': 10},
                   {'hour': 8, 'minute': 57, 'second': 12, 'AM/PM':'AM'}],
    },
}

def test_ampm():
    """Test state machines used for finding 'am', 'pm', 'AM', or 'PM' in free text"""
    for txt, dct in TESTIO.items():
        _run_ampm(txt, dct['exp_dct'])


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
    test_ampm()
    print(white(f'{timedelta(seconds=default_timer()-tic_all)} TOTAL TIME FOR ALL TESTS'))
