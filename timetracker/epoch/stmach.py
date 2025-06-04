"""Examine free text representing a timedelta or a datetime"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"


DIGITS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

class _SmHhSsAm:
    """State machine to find HH:SSam, HHam, and variations"""

    def __init__(self):
        self.name = 'HH:SS:am'
        self.capture = None
        self.state = 'start'
        self.found = False
        self.dfa = {
            'start': self._dfa_h1,
            'h1':    self._dfa_h2,
            'h2':    self._dfa_after_h2,
            's10':   self._dfa_s10,
            's1':    self._dfa_s1,
            'AP':    self._dfa_ap,
            'm':     self._dfa_ampm_m,
            'M':     self._dfa_ampm_m,
        }

    def get_match(self):
        r"""Get the items from matching '\d{1,2}(:\d\d)?(am|AM|pm|PM)'"""
        capture = self.capture
        if capture is None:
            return None
        if 'AM/PM' not in capture:
            return None
        ##print(f'CAPTURE({capture})')
        ret = {'HH': int(''.join(capture['HH']))}
        if 'SS' in capture:
            ret['SS'] = int(''.join(capture['SS']))
        ret['AM/PM'] = ''.join(capture['AM/PM'])
        return ret

    def run(self, letter):
        """Run the discrete state machine to search for pattern"""
        state = self.dfa[self.state](letter)
        print(f'StateMachine-{self.name} FOUND({int(self.found)}) LETTER({letter}) '
              f'STCUR({self.state}) STNXT({state})')
        if self.capture is not None and state == 'matched':
            ##self.capture = f'{self.capture}m'
            ##fnc_docapture()
            self.found = True
        self.state = state
        print(f'RESULT: {letter} {self}\n')
        return state != 'matched'

    def __str__(self):
        return f'{self.name} {int(self.found)} ST({self.state}) {self.capture}'

    def _dfa_ampm_start(self, letter):
        """A Discrete State Atomaton in the discrete state machine to find AM/PM"""
        if letter in {'a', 'p'}:
            self.capture['AM/PM'] = [letter.upper()]
            return 'm'
        if letter in {'A', 'P'}:
            self.capture['AM/PM'] = [letter]
            return 'M'
        return 'start'

    def _dfa_ampm_m(self, letter):
        if letter in {'m', 'M'}:
            self.capture['AM/PM'].append('M')
            self.found = True
            return 'matched'
        return 'start'

    def _dfa_s10(self, letter):
        if letter in DIGITS:
            self.capture['SS'] = [letter]
            return 's1'
        return 'start'

    def _dfa_s1(self, letter):
        if letter in DIGITS:
            self.capture['SS'].append(letter)
            return 'AP'
        return 'start'

    def _dfa_h1(self, letter):
        if letter in DIGITS:
            self.capture = {'HH': [letter]}
            return 'h1'
        return 'start'

    def _dfa_h2(self, letter):
        if letter in DIGITS:
            self.capture['HH'].append(letter)
            return 'h2'
        return self._dfa_after_h2(letter)

    def _dfa_after_h2(self, letter):
        if letter == ':':
            return 's10'
        return self._dfa_ap(letter)

    def _dfa_ap(self, letter):
        if letter in {'a', 'p'}:
            self.capture['AM/PM'] = [letter.upper()]
            return 'm'
        if letter in {'A', 'P'}:
            self.capture['AM/PM'] = [letter]
            return 'M'
        return 'start'


def search_texttime(txt):
    """Search for HH:SSam, HHam, and variations"""
    num_colons = 0
    smo = _SmHhSsAm()
    for letter_cur in txt:
        if not smo.found:
            smo.run(letter_cur)
        if letter_cur == ':':
            num_colons += 1
    if num_colons >= 2:
        return None
    return smo.get_match()


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
