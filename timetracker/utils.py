"""Utilities for configuration parser"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"


def red(txt):
    """Return the text, colored yellow"""
    return _color_fg(1, txt)

def redorange(txt):
    """Return the text, colored yellow"""
    return _color_fg(196, txt)

def yellow(txt):
    """Return the text, colored yellow"""
    return _color_fg(11, txt)

def pink(txt):
    """Return the text, colored pink"""
    return _color_fg(13, txt)

def orange(txt):
    """Return the text, colored orange"""
    return _color_fg(9, txt)

def ltblue(txt):
    """Return the text, colored orange"""
    return _color_fg(12, txt)

def white(txt):
    """Return the text, colored orange"""
    return _color_fg(15, txt)

def cyan(txt):
    """Return the text, colored orange"""
    return _color_fg(14, txt)

def prt_todo(msg):
    """Return an eye-catching TODO string"""
    print(_color_fgbg(11, 0, 1,
        f'{msg}:\nOpen an issue at: '
        'https://github.com/dvklopfenstein/timetracker/issues'))

def _color_fg(colornum, txt):
    """Return the text, colorized"""
    return f"\x1b[48;5;0;38;5;{colornum};1;1m{txt}\x1b[0m"

def _color_fgbg(fgcolor, bgcolor, code, txt):
    """Return the text, colorized"""
    return f"\x1b[48;5;{bgcolor};38;5;{fgcolor};1;{code}m{txt}\x1b[0m"


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
