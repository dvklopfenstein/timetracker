"""Command line interface (CLI) for one of starttime, stoptime, and span, given two"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from sys import argv as sys_argv
from argparse import ArgumentParser
from argparse import ArgumentDefaultsHelpFormatter
from timetracker.epoch.epoch import get_dt_or_td
from timetracker.epoch.epoch import get_dtb


def main(args=None):
    """Connect all parts of the timetracker"""
    args = get_args(args)
    #print(f'ARGS: {args}')
    obj = TimeCalc23(args.timestr1, args.timestr2)
    result = obj.calc()
    obj.print(result)

class TimeCalc23:
    """Command line interface (CLI) for one of starttime, stoptime, and span, given two"""

    def __init__(self, timestr1, timestr2):
        self.timestr1 = timestr1
        self.timestr2 = timestr2
        self.time1 = get_dt_or_td(timestr1)
        self.time2 = get_dt_or_td(timestr2)
        self.maxlen = max(len(timestr1), len(timestr2))
        self.dts = []
        self.tdo = None
        self._init_time(self.timestr1, self.time1)
        self._init_time(self.timestr2, self.time2)

    def _init_time(self, txt, dct):
        """Add a datetime object or a timedelta object"""
        if dct:
            if (key := next(iter(dct))) == 'datetime':
                if len(self.dts) in {0, 1}:
                    self.dts.append(dct['datetime'])
                    dct['timeobj'] = f"{txt:{self.maxlen}} -> {dct['datetime']}"
                else:
                    raise ValueError('ONLY TWO datetime OBJECTS PERMITTED')
            else:
                assert key == 'timedelta'
                if self.tdo is None:
                    self.tdo = dct['timedelta']
                    dct['timeobj'] = f"{txt:{self.maxlen}} -> {dct['timedelta']:,} seconds"
                else:
                    raise ValueError(f'timedelta ALREADY EXISTS: {self.tdo}')

    def calc(self):
        """Calculate the third value, given two of: starttime, stoptime, or span"""
        if (num_dts := len(self.dts)) == 1 and self.tdo is not None:
            return get_dtb(self.dts[0], self.tdo)
        if num_dts == 2:
            dts = sorted(self.dts)
            return dts[1] - dts[0]
        return None

    def print(self, result):
        """Print arguments in and out and the results"""
        if result is None:
            return
        print(f"ARG1: {self.time1['timeobj']}")
        print(f"ARG2: {self.time2['timeobj']}")
        spc = ""
        print(f'RESULT{spc:{self.maxlen}} -> {result}')



def get_args(args=None):
    """Get args for calculating one of: starttime, stoptime, or span"""
    parser = _init_parser()
    args = sys_argv[1:] if args is None else args
    args = [f" {val}" if val[:1] == '-' else val for val in args]
    return parser.parse_args(args)

def _init_parser():
    """Create the top-level parser"""
    parser = ArgumentParser(
        prog='timecalc',
        description="Calculate starttime, stoptime, or span, given two of the three.",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('timestr1',
        help='One from: starttime or stoptime(eg "9:20am"), or span("40min")')
    parser.add_argument('timestr2',
        help='One from: starttime, stoptime(eg "2025-07-05 9am"), or span')
    return parser


if __name__ == '__main__':
    main()

# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
