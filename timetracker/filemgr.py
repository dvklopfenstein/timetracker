"""File manager"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists


class FileMgr:
    """File manager"""
    # pylint: disable=too-few-public-methods

    def __init__(self, cfg_local, cfg_global, **kws):
        self.cfg = cfg_local
        self.cfg_global = cfg_global
        self.name = kws['name']      # From Reasearcher's USER envvar
        self.kws = kws

    def exists_workdir(self):
        """Test existance of timetracker working directory"""
        return exists(self.kws['trksubdir'])

    ##def str_tags(self):
    ##    """Get the stop-timer tags"""
    ##    tags = self.kws['tags']
    ##    if not tags:
    ##        return ''
    ##    return ';'.join(tags)

    ##def workdir_exists(self):
    ##    return isdir(self.get_dirname_work())

    ##def get_dirname_work(self):
    ##    return join('.', self.tdir)

    ##def __str__(self):
    ##    return (
    ##        f'IniFile FILENAME: {self.cfgfile}'
    ##        f'IniFile USER:     {self.name}'
    ##    )

    ##def _init_cfgname(self):
    ##    """Get the config file from the config search path"""
    ##    for cfgname in self._get_cfg_searchpath():
    ##        if cfgname is not None and isfile(cfgname):
    ##            return cfgname
    ##    return None

    ##def _get_cfg_searchpath(self):
    ##    """Get config search path"""
    ##    return [
    ##        # 1. Local directory
    ##        join('.', self.tdir, '/config'),
    ##        # 2. Home directory:
    ##        expanduser(join('~', self.tdir, 'config')),
    ##        expanduser(join('~', '.config', 'timetracker.conf')),
    ##        # 3. System-wide directory:
    ##        '/etc/timetracker/config',
    ##        # 4. Environmental variable:
    ##        environ.get('TIMETRACKERCONF'),
    ##    ]


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
