"""Utilities for configuration parser"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"


def yellow(txt):
    """Return the text, colored yellow"""
    return _color(txt, 11)

def pink(txt):
    """Return the text, colored pink"""
    return _color(txt, 13)

def orange(txt):
    """Return the text, colored orange"""
    return _color(txt, 9)

def ltblue(txt):
    """Return the text, colored orange"""
    return _color(txt, 12)

def white(txt):
    """Return the text, colored orange"""
    return _color(txt, 15)

def _color(txt, colornum):
    """Return the text, colorized"""
    return f"\x1b[48;5;0;38;5;{colornum};1;1m{txt:5}\x1b[0m"


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
