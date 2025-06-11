#!/usr/bin/env python3
"""Test state machines used for finding datetime in free text"""

from timeit import default_timer
from datetime import timedelta
from timetracker.utils import white
from timetracker.utils import yellow
from timetracker.epoch.stmach import search_texttime


def test_sm_hhss_am():
    """Test state machines used for finding 'am', 'pm', 'AM', or 'PM' in free text"""
    tic = default_timer()
    _run('5pm',     exp={'hour': 17})
    _run('5:30pm',  exp={'hour': 17, 'minute': 30})
    _run(txt='ampm',          exp=None)
    _run(txt='13:23:00',      exp={'hour': 13, 'minute': 23, 'second': 0})
    #_run(txt='13 :23 :00 :a', exp=None)
    _run(txt='12',            exp={'hour': 12})
    _run(txt='1',             exp={'hour':  1})
    print(white(f'{timedelta(seconds=default_timer()-tic)} TOTAL TIME'))

def _run_time(time, exp):
    _run(f'{time}',           exp)
    _run(f'{time} 3am',       exp)
    _run(f'{time} a 3am a ',  exp)
    _run(f'{time} xtra txt',  exp)

def _run(txt, exp):
    print(yellow(f'\nTRY TEXT({txt})'))
    tic = default_timer()
    act = search_texttime(txt)
    print(white(f'{timedelta(seconds=default_timer()-tic)} RESULT({act})'))
    assert act == exp, f'TXT({txt})\nTXT({txt}) -> EXP({exp})\nTXT({txt}) -> ACT({act})'


if __name__ == '__main__':
    test_sm_hhss_am()
