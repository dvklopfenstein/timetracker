"""File manager"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

##from os import environ
from os.path import exists
##from os.path import isdir
from os.path import join
##from os.path import isfile
##from os.path import expanduser
##from configparser import ConfigParser


class FileMgr:
    """File manager"""
    # pylint: disable=too-few-public-methods

    ##def __init__(self):
    ##    self.tdir = '.timetracker'
    ##    self.cfgfile = self._init_cfgname()
    ##    print(f'INITFILE: {self.cfgfile}')
    ##    self.name = environ.get('USER')

    def __init__(self, **kws):
        self.tdir = kws['directory']
        self.name = kws['name']
        self.kws = kws

    def get_workdir(self):
        """Get directory for timetracker information"""
        return self.tdir

    def exists_workdir(self):
        """Test existance of timetracker working directory"""
        return exists(self.tdir)

    def get_filename_start(self):
        """Get the file storing the start time a person"""
        return join(self.tdir, f'start_{self.name}.txt')

    def force(self):
        """Return the value of force"""
        return self.kws.get('force', False)

    ##def workdir_exists(self):
    ##    return isdir(self.get_dirname_work())

    ##def get_dirname_work(self):
    ##    return join('.', self.tdir)

    ##def get_filename_start(self):
    ##    """Get the filename where the start time is written"""
    ##    return join(self.get_dirname_work(), f'start_time_{self.name}.txt')

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
