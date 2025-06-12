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
    """In free text, find HH:SSam, HHam, and variations"""

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
                self.stnum = 4
                return 'year'
        elif self.stnum == 4:
            self.capture['year'] = int(''.join(self.work))
            self.stnum = None
        # Process non-digit
        if letter in {'-', '_', '/'}:
            return 'month'
        return 'start'

    def _dfa_month(self, letter):
        if self._run_onetwodigit(letter):
            return 'month'
        if letter in {'-', '_', '/'} and 1 <= (month := int(''.join(self.work))) <= 12:
            self.capture['month'] = month
            self.stnum = None
            return 'day'
        return 'start'

    def _dfa_day(self, letter):
        if self._run_onetwodigit(letter):
            return 'day'
        if 1 <= (day := int(''.join(self.work))) <= 31:
            self.capture['day'] = day
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
    def run(self, stval, letter):
        """Run the discrete sm to search for pattern"""
        msg = (f'LETTER({letter}) '
               f'STCUR({stval} {self.stnum}) '
               f'WORK({self.work}) '
               f'LETTER({letter})')
        #print('MSG:', msg)
        stval = self.dfa[stval](letter)
        print(f'SM {msg} WORK({self.work}) STNXT({stval}) CAPTURE({self.capture})')
        return stval

    def finish(self):
        """Finish finding time in text formatted as '5pm', '5:32am', '5:00:00', etc."""
        capture = self.capture
        print(f'CAPTURE @ FINISH: {capture}')
        # Require that the hour is specified
        if 'hour' not in capture:
            self.capture = None
        # Add 12 hours if 'pm'
        if (ampm := capture.get('AM/PM')) is not None:
            del self.capture['AM/PM']
            if ampm == 'PM':
                if 0 <= (hour := capture['hour']) < 12:
                    capture['hour'] = hour + 12
                elif hour != 12:
                    self.capture = None
            else:
                assert ampm == 'AM', capture
                if capture['hour'] == 12:
                    capture['hour'] = 0
        # Accept whole dates (YYYY-MM-DD) or none at all
        if not {'year', 'month', 'day'}.issubset((keyset := set(capture.keys()))) and \
           not {'year', 'month', 'day'}.isdisjoint(keyset):
            self.capture = None
        # Keep "nothing captured" consistent
        if not capture:
            self.capture = None


def search_texttime(txt):
    """Search for HH:SSam, HHam, and variations"""
    num_colons = 0
    smo = _SmHhSsAm()
    stval = 'start'
    for letter in txt:
        stval = smo.run(stval, letter)
    smo.run(stval, None)
    smo.finish()
    if num_colons >= 2:
        return None
    return smo.capture


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
