"""Configuration manager for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import environ
from os.path import isfile
from os.path import expanduser
from configparser import ConfigParser


class Cfg:
    """Configuration manager for timetracking"""
    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.cfg = self._init_cfg()

    def _init_cfg(self):
        cfg = ConfigParser()
        return cfg

    def get_cfgfile(self):
        """Get the config file from the config search path"""
        for cfgname in self._get_cfg_searchpath():
            if cfgname is not None and isfile(cfgname):
                return cfgname
        return None

    def _get_cfg_searchpath(self):
        """Get config search path"""
        return [
            # 1. Local directory
            './.timetracker/config',
            # 2. Home directory:
            expanduser('~/.timetracker/config'),
            expanduser('~/.config/timetracker.conf'),
            # 3. System-wide directory:
            '/etc/timetracker/config',
            # 4. Environmental variable:
            environ.get('TIMETRACKERCONF'),
        ]




# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
