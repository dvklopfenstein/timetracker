#!/usr/bin/env python3
"""Test state machines used for finding datetime in free text"""

from timeit import default_timer
from datetime import timedelta
from timetracker.epoch.stmach import ampm_examine
from timetracker.utils import white


def test_ampm():
    """Test state machines used for finding datetime in free text"""
    _run(txt='5pm',          exp={'num_ampma': 1, 'num_colons': 0})
    _run(txt='5pm xtra txt', exp={'num_ampma': 1, 'num_colons': 0})
    _run(txt='ampm',         exp={'num_ampma': 1, 'num_colons': 0})
    _run(txt='13:23:00',     exp={'num_ampma': 0, 'num_colons': 2})

def _run(txt, exp):
    print(white(f'\nTRY TEXT({txt})'))
    tic = default_timer()
    act = ampm_examine(txt)
    print(white(f'{timedelta(seconds=default_timer()-tic)} RESULT({act})'))
    assert act == exp, f'TXT({txt})\nTXT({txt}) -> EXP({exp})\nTXT({txt}) -> ACT({act})'


if __name__ == '__main__':
    test_ampm()
