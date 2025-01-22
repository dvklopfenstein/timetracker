"""Configuration manager for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import environ
from configparser import ConfigParser


class Cfg:
    """Configuration manager for timetracking"""
    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.cfg = self._init_cfg()
        self.name = environ.get('USER')

    def _init_cfg(self):
        cfg = ConfigParser()
        return cfg


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
