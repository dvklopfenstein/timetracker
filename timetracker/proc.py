"""Run processes and subprocesses"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from subprocess import run
from shutil import which
from collections import namedtuple


def get_gitusername():
    """Get the git user.name from the config"""
    cmd = 'git config user.name'.split()
    return _run_git_cmd(cmd).stdout

def git_commit_file(filename, message):
    """git commit a file"""
    cmd = ['git', 'commit', filename, '-m', message]
    return _run_git_cmd(cmd)

def get_log1():
    """Get the last git log with pretty print"""
    cmd = ['git', 'log', '-1', '--pretty=%B']
    return _run_git_cmd(cmd)

def _run_git_cmd(cmdlst):
    """Run a git command"""
    if which('git') is not None:
        #print(f'CMD: {cmdlst}')
        rsp = run(cmdlst, capture_output=True, check=False)
        #print(f'RSP: {dir(rsp)}')
        if rsp:
            nto = namedtuple('NtCmpPrc', 'returncode stderr stdout')
            ntd = nto(
                returncode=rsp.returncode,
                stderr=None if rsp.stderr == b'' else rsp.stderr.decode('utf-8').strip(),
                stdout=None if rsp.stdout == b'' else rsp.stdout.decode('utf-8').strip())
            #print(f'({ntd})')
            return ntd
    return None


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
