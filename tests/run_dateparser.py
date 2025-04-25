#!/usr/bin/env python3
"""Run epoch.cli using dateparser, rather than dateutil"""
# Note: consider [Python datetimes made easy](https://github.com/python-pendulum/pendulum)

from logging import basicConfig, DEBUG
from timetracker.epoch.cli import main
basicConfig(level=DEBUG)


if __name__ == '__main__':
    main()
