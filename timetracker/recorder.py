"""Track your time; record it in a csv file"""

__copyright__ = 'Copyright (C) 2025, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from os.path import exists
from logging import info
from logging import warning
from logging import error
from timeit import default_timer
from datetime import timedelta
from datetime import datetime


class Recorder:
    """Track your time; record it in a csv file"""

    datpat = '%Y-%m-%d %H:%M:%S.%f'

    def __init__(self, csv_filename, startfile='.timetracker_starttime'):
        self.csv = csv_filename
        self.startfile = startfile

    def start(self):
        """Append the starting time in the csv file"""
        tic = default_timer()
        t0_txt = self._rd_startfile()
        if t0_txt is not None:
            warning(f'OVER-WRITING START TIME({t0_txt}) WITH {tic}')
        with open(self.startfile, 'w', encoding='utf8') as prt:
            prt.write(f'{tic} {datetime.now()}')
            info(f'{tic}  WROTE: {self.startfile}')

    def stop(self, description):
        """Append the stop time and message in the csv file"""
        tic, dt0 = self._rd_datetime()
        if tic is None:
            error('NOT WRITING ELAPSED TIME; NO STARTING TIME FOUND')
            return
        toc = default_timer()
        dtx = datetime.now()
        delta = f'{timedelta(seconds=toc-tic)}'
        tags = ''
        if not exists(self.csv):
            self._wr_csvhdrs()
        with open(self.csv, 'a', encoding='utf8') as prt:
            prt.write(f'{dt0.strftime("%a")},{dt0},{tic},'
                      f'{dtx.strftime("%a")},{dtx},{toc},'
                      f'{tags},{delta},{description}\n')
            info(f'Elapsed H:M:S={delta} APPENDED TO {self.csv}')
        ##print(f'{dt0} {tic}  START')
        ##print(f'{dtx} {toc}  STOP  {description}')

    def _wr_csvhdrs(self):
        # aTimeLogger columns: Activity From To Notes
        with open(self.csv, 'w', encoding='utf8') as prt:
            prt.write('start_day,'
                      'start_datetime,'
                      'start_tic,'
                      'stop_day,'
                      'stop_datetime,'
                      'stop_toc,'
                      'duration,'
                      'tags,'
                      'type,'
                      'comment\n')

    def _rd_datetime(self):
        txt = self._rd_startfile()
        pt0 = txt.find(' ')
        tic = self._get_float(txt[:pt0])
        if tic is not None:
            return tic, datetime.strptime(txt[pt0+1:], self.datpat)
        return None, None

    def _get_float(self, float_str):
        try:
            return float(float_str)
        except ValueError:
            warning(f'START TIME({float_str}) IS NOT A FLOATING POINT NUMBER')
            return None

    def _rd_startfile(self):
        if exists(self.startfile):
            with open(self.startfile, encoding='utf8') as ifstrm:
                return ''.join(ifstrm.readlines())
        return None


# Copyright (C) 2025, DV Klopfenstein, PhD. All rights reserved.
