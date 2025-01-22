"""Run processes and subprocesses"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from subprocess import run
from shutil import which


def get_gitusername():
    """Get the git user.name from the config"""
    if which('git') is not None:
        cmd = 'git config user.name'
        ##print(f'CMD: {cmd}')
        rsp = run(cmd.split(), capture_output=True, check=False)
        if rsp.returncode == 0 and rsp.stderr == b'':
            name = rsp.stdout.decode('utf-8').strip()
            ##print(f'({name})')
            ##print(rsp)
            return name
    return None


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
