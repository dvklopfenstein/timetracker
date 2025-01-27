"""File manager"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os import makedirs
from os import remove
from os.path import exists
from os.path import abspath
from timetracker.hms import hms_from_startfile


class FileMgr:
    """File manager"""
    # pylint: disable=too-few-public-methods

    def __init__(self, cfg, **kws):
        self.cfg = cfg
        self.tdir = kws['directory']
        self.name = kws['name']
        self.kws = kws

    def get(self, key):
        """Get a argument value.
        Given:
            forced:   `start` test feature
            message:  `stop`  required message upon printing a stop time
            activity: `stop`  activity written into csv
            activity: `stop`  test feature; keep start time instead of resetting
        """
        return self.kws.get(key)

    def get_workdir(self):
        """Get directory for timetracker information"""
        return self.tdir

    def ini_workdir(self):
        """Initialize timetracker working directory"""
        dirtrk = self.get_workdir()
        if not exists(dirtrk):
            makedirs(dirtrk, exist_ok=True)
            absdir = abspath(dirtrk)
            if not self.kws.get('quiet'):
                print(f'Initialized timetracker directory: {absdir}')

    def exists_workdir(self):
        """Test existance of timetracker working directory"""
        return exists(self.tdir)

    ####def get_filename_start(self):
    ####    """Get the file storing the start time a person"""
    ####    return join(self.tdir, f'start_{self.name}.txt')

    def rm_starttime(self):
        """Remove the starttime file, thus resetting the timer"""
        fstart = self.cfg.get_filename_start()
        if exists(fstart):
            remove(fstart)

    def prt_elapsed(self):
        """Print elapsed time if timer is started"""
        fin_start = self.cfg.get_filename_start()
        # Print elapsed time, if timer was started
        if exists(fin_start):
            hms = hms_from_startfile(fin_start)
            print(f'\nTimer running: {hms} H:M:S '
                  f'elapsed time for name({self.name}) '
                  f'project({self.cfg.project})')

    def str_tags(self):
        """Get the stop-timer tags"""
        tags = self.kws['tags']
        if not tags:
            return ''
        return ';'.join(tags)

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
