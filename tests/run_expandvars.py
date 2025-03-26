#!/usr/bin/env python3
"""Print environmental variables which may be used in config files in the future"""

from os import environ
from os import getcwd
#from os import access
from os.path import isdir
from os.path import exists
#from filecmp import dircmp
from logging import basicConfig, DEBUG
basicConfig(level=DEBUG)

def main():
    """Print environmental variables which may be used in config files in the future"""
    cwd = getcwd()
    for key, val in environ.items():
        if isdir(val) and exists(val):
            #vlen = len(val)
            if cwd[:len(val)] == val:
                print(f'{key:30} {val}')
                #dco = dircmp(cwd, val)
                #print(f'COMMON: {dco.common_dirs}')
    print(f'CWD: {cwd}')


if __name__ == '__main__':
    main()
