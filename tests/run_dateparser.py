#!/usr/bin/env python3
"""Run epoch.cli using dateparser, rather than dateutil"""

from logging import basicConfig, DEBUG
from timetracker.epoch.cli import main
basicConfig(level=DEBUG)


if __name__ == '__main__':
    main()
