#!/usr/bin/env python3
"""Various tests when the project config file does not exist"""

from logging import basicConfig
from logging import DEBUG
from tempfile import TemporaryDirectory
from tests.pkgtttest.runfncs import proj_setup


basicConfig(level=DEBUG)

SEP = f'\n{"="*80}\n'

def test_get_filename_csv(project='apples', dircur='dirproj', username='piemaker'):
    """Test getting a csv name when the project config file does not exist"""
    with TemporaryDirectory() as tmphome:
        _, _, _ = proj_setup(tmphome, project, dircur, dirgit01=True)
        assert username


if __name__ == '__main__':
    test_get_filename_csv()
