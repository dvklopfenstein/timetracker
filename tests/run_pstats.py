#!/usr/bin/env python3
"""Run pstats to analyze cProfile results"""

from pstats import Stats


def main():
    """Print the 50 lines with the logest cumulative duration"""
    prof = Stats('profile')
    #prof.strip_dirs()
    prof.sort_stats('cumtime')
    prof.print_stats(50)


if __name__ == '__main__':
    main()
