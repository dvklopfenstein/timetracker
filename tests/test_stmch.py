#!/usr/bin/env python3
"""Test state machines used for finding datetime in free text"""

from datetime import datetime
from datetime import timedelta
from timeit import default_timer
from timetracker.utils import white
from timetracker.epoch.stmach import _SmHhSsAm
from timetracker.epoch.epoch import get_dt_ampm

NOW = datetime.today()

TESTIO = {
    '12am':{
        'exp_dct':[{'hour': 12, 'AM/PM': 'AM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 0, 0, 0)
    },

    '12pm':{
        'exp_dct':[{'hour': 12, 'AM/PM': 'PM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 12, 0, 0)
    },

    '12:01am':{
        'exp_dct':[{'hour': 12, 'AM/PM': 'AM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 0, 1, 0)
    },

    '12:01pm':{
        'exp_dct':[{'hour': 12, 'AM/PM': 'PM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 12, 1, 0)
    },

    '13pm':{
        'exp_dct':[{'hour': 13, 'AM/PM': 'PM'}],
        'dt': None,
    },

    '5pm':{
        'exp_dct':[{'hour':5, 'AM/PM':'PM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 17, 0, 0)
    },

    '5pm 3am':{
        'exp_dct':[{'hour':5, 'AM/PM':'PM'},
                   {'hour':3, 'AM/PM':'AM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 3, 0, 0),
    },

    '5pm a 3am a ':{
        'exp_dct':[{'hour':5, 'AM/PM':'PM'},
                   {'hour':3, 'AM/PM':'AM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 3, 0, 0),
    },

    '5pm xtra txt':{
        'exp_dct':[{'hour':5, 'AM/PM':'PM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 17, 0, 0),
    },

    'ampm':{'exp_dct':[], 'dt':None},

    '13:23:00':{
        'exp_dct':[{'hour':13, 'minute': 23, 'second': 0}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 13, 23, 0),
    },

    '2025':{
        'exp_dct':[{'year': 2025}],
        'dt': None,
    },

    '2025-06-10 08:57:12 AM':{
        'exp_dct':[{'year': 2025, 'month': 6, 'day': 10},
                   {'hour': 8, 'minute': 57, 'second': 12, 'AM/PM':'AM'}],
        'dt': datetime(2025, 6, 10, 8, 57, 12),
    },

    '2025-06-10 8:57:12am':{
        'exp_dct':[{'year': 2025, 'month': 6, 'day': 10},
                   {'hour': 8, 'minute': 57, 'second': 12, 'AM/PM':'AM'}],
        'dt': datetime(2025, 6, 10, 8, 57, 12),
    },
}

def test_ampm():
    """Test state machines used for finding 'am', 'pm', 'AM', or 'PM' in free text"""
    for txt, dct in TESTIO.items():
        #_run_ampm(txt, dct['exp_dct'])
        act = get_dt_ampm(txt, None)
        assert act == dct['dt'], ('EXP != ACT:\n'
            f'  TXT: {txt}\n'
            f'  EXP: {dct["dt"]}\n'
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
    test_ampm()
    print(white(f'{timedelta(seconds=default_timer()-tic_all)} TOTAL TIME FOR ALL TESTS'))
