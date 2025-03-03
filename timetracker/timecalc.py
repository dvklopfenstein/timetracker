"""Time calculations"""
# 2016 https://pyinterval.readthedocs.io/en/latest/guide.html
#      https://github.com/taschini/pyinterval
# 2024 https://github.com/AlexandreDecan/portion (482 stars)
#      https://pypi.org/project/portion/
#      https://pypi.org/project/python-intervals/ (2020)
# NNNN https://mauriciopoppe.github.io/interval-arithmetic/
#      https://www.mauriciopoppe.com/notes/computer-science/programming-languages/cpp-refresher/
# 2022 https://github.com/mauriciopoppe
# 2025 https://github.com/flintlib/flint/
# 2018 https://github.com/loliGothicK/Cranberries ARCHIVED

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

from datetime import datetime
from datetime import timedelta


def timedelta_to_hms(tdelta):
    """Convert a timedelta to hours and minutes"""
    total_secs = tdelta.total_seconds()
    assert total_secs >= 0, total_secs
    hours, remainder = divmod(total_secs, 3600)
    minutes, seconds = divmod(remainder, 60)
    return int(hours), int(minutes), seconds

def _totsecs_to_hms(total_secs):
    """Convert a timedelta to hours and minutes"""
    hours, remainder = divmod(total_secs, 3600)
    minutes, seconds = divmod(remainder, 60)
    return int(hours), int(minutes), seconds

def str_td(tdelta):
    """Convert a tuple containing hours, minutes, and seconds to a string"""
    total_secs = tdelta.total_seconds()
    return _secspos_to_str(total_secs) if total_secs >= 0 else _secsneg_to_str(total_secs)

def _secspos_to_str(total_secs):
    """Convert a tuple containing hours, minutes, and seconds to a string"""
    cur_hours, cur_minutes, _ = _totsecs_to_hms(total_secs)
    return f'{cur_hours:02}:{cur_minutes:02}'

def _secsneg_to_str(total_secs):
    """Convert a tuple containing hours, minutes, and seconds to a string"""
    cur_hours, cur_minutes, _ = _totsecs_to_hms(-total_secs)
    return f'-{cur_hours:02}:{cur_minutes:02}'


class RoundTime:
    """Round a datetime object up or down to `round_to_min`"""
    # pylint: disable=line-too-long
    # https://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object/10854034#10854034
    # Answered by: https://stackoverflow.com/users/7771076/ofo

    def __init__(self, round_to_min=15, epoch_ref=None):
        self.round_to_min = round_to_min
        self.reftime = datetime(1970, 1, 1, tzinfo=datetime.now().tzinfo) if epoch_ref is None else epoch_ref
        self.tdroundval = timedelta(minutes=round_to_min)

    def _time_mod(self, time):
        return (time - self.reftime) % self.tdroundval

    def time_round(self, time):
        """Round a datetime object up or down to the minutes specified in round_to_min"""
        mod = self._time_mod(time)
        return time - mod if mod < self.tdroundval/2 else time + (self.tdroundval - mod)

    def time_floor(self, time):
        """Round a datetime object up to the minutes specified in round_to_min"""
        return time - self._time_mod(time)

    def time_ceil(self, time):
        """Round a datetime object down to the minutes specified in round_to_min"""
        mod = self._time_mod(time)
        return time + (self.tdroundval - mod) if mod else time


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
