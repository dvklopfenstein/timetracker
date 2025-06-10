"""Examine free text representing a timedelta or a datetime"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

# NOTE:
# 24:00 refers to midnight at the end of a given date
# 00:00 refers to the beginning of the day

##from timetracker.epoch.sm_ampm import run_ampm
##from timetracker.epoch.sm_ampm import get_match_ampm
##from timetracker.epoch.sm_ampm import FOUND_AMPM


DIGITS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

class _SmHhSsAm:
    """State machine to find HH:SSam, HHam, and variations"""

    def __init__(self):
        self.capture = {}
        self.work = None
        self.stnum = None
        self.dfa = {
            'start':  self._dfa_start,
            'digits': self._dfa_digits,  # year or hour
            'minute': self._dfa_min,
            'second': self._dfa_sec,
            'AM/PM':  self._dfa_ampm,
            'year':   self._dfa_year,
            'month':  self._dfa_month,
            'day':    self._dfa_day,
        }

    def _dfa_start(self, letter):
        if letter in DIGITS:
            self.work = [letter,]
            self.stnum = '1'
            return 'digits'
        return 'start'

    def _dfa_digits(self, letter):
        if letter in DIGITS:
            if self.stnum == '1':
                self.work.append(letter)
                self.stnum = '2'
                return 'digits'
            if self.stnum == '2':
                self.work.append(letter)
                self.stnum = '3'
                return 'year'
            assert f'UNEXPECTED HOUR OR YEAR DIGIT({letter})'
        elif self.stnum in {'1', '2'}:
            if (hour := int(''.join(self.work))) <= 24:
                self.capture['hour'] = hour
                self.stnum = None
            else:
                return 'start'
        # Process non-digit
        if letter == ':':
            return 'minute'
        return self._run_ap(letter)

    def _dfa_min(self, letter):
        if self._run_onetwodigit(letter):
            return 'minute'
        if self.stnum in {'1', '2'}:
            if (minute := int(''.join(self.work))) <= 60:
                self.capture['minute'] = minute
                self.stnum = None
            else:
                return 'start'
        # Process non-digit
        if letter == ':':
            return 'second'
        return self._run_ap(letter)

    def _dfa_sec(self, letter):
        if self._run_onetwodigit(letter):
            return 'second'
        if self.stnum in {'1', '2'}:
            if (minute := int(''.join(self.work))) <= 60:
                self.capture['second'] = minute
                self.stnum = None
            else:
                return 'start'
        # Process non-digit
        return self._run_ap(letter)

    def _run_ap(self, letter):
        if letter in {'a', 'A', 'p', 'P', ' '}:
            if letter != ' ':
                self.work = letter.upper()
            else:
                self.work = None
            return 'AM/PM'
        return 'start'

    def _dfa_ampm(self, letter):
        if letter in {'m', 'M'} and self.work:
            self.capture['AM/PM'] = f'{self.work}M'
        return self._run_ap(letter)

    def _dfa_year(self, letter):
        if letter in DIGITS:
            if self.stnum == '3':
                self.work.append(letter)
                self.capture['year'] = int(''.join(self.work))
                self.stnum = None
                return 'year'
        elif letter in {'-', '_', '/'}:
            return 'month'
        return 'start'

    def _dfa_month(self, letter):
        if self._run_onetwodigit(letter):
            return 'month'
        if letter in {'-', '_', '/'}:
            self.capture['month'] = int(''.join(self.work))
            self.stnum = None
            return 'day'
        return 'start'

    def _dfa_day(self, letter):
        if self._run_onetwodigit(letter):
            return 'day'
        self.capture['day'] = int(''.join(self.work))
        self.stnum = None
        return 'start'

    # -------------------------------------------------------------------
    def _run_onetwodigit(self, letter):
        if letter in DIGITS:
            if self.stnum is None:
                self.stnum = '1'
                self.work = [letter,]
                return True
            if self.stnum == '1':
                self.stnum = '2'
                self.work.append(letter)
                return True
            assert f'UNEXPECTED 1st OR 2nd DIGIT({letter})'
        return False

    # -------------------------------------------------------------------
    def run(self, state, letter):
        """Run the discrete state machine to search for pattern"""
        msg = (f'LETTER({letter}) '
               f'STCUR({state} {self.stnum}) '
               f'WORK({self.work}) ' 
               f'LETTER({letter})')
        #print('MSG:', msg)
        state = self.dfa[state](letter)
        print(f'StateMachine {msg} '
              f'WORK({self.work}) '
              f'STNXT({state}) '
              f'CAPTURE({self.capture})')
        return state

def search_texttime(txt):
    """Search for HH:SSam, HHam, and variations"""
    num_colons = 0
    smo = _SmHhSsAm()
    state = 'start'
    for letter in txt:
        state = smo.run(state, letter)
    smo.run(state, None)
    if num_colons >= 2:
        return None
    return smo.capture
    ##return get_match_ampm()
    ##return None

####def get_match(self):
####    r"""Get the items from matching '\d{1,2}(:\d\d)?(am|AM|pm|PM)'"""
####    capture = self.capture
####    if capture is None:
####        return None
####    if 'AM/PM' not in capture:
####        return None
####    hour = int(''.join(capture['HH']))
####    if capture['AM/PM'] == ['P', 'M']:
####        hour += 12
####    ret = {'HH': hour}
####    if 'SS' in capture:
####        ret['SS'] = int(''.join(capture['SS']))
####    return ret


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
