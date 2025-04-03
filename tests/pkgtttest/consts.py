"""Checks for Finder values"""

SEP1 = f'{"="*80}\n'
SEP2 = f'{"-"*80}\n'
SEP3 = f'{"- "*40}\n'

def sep_test(test_num, char='='):
    """Get separator with test number inserted"""
    return f'{char*4} TEST {test_num} {char*70}\n'
