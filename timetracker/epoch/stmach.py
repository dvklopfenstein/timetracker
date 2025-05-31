"""Examine free text representing a timedelta or a datetime"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"


class _SmAmPm:
    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.capture = None
        self.num_ampms = 0
        self.dfa_am_pm = {
            'start': self._dfa_ampm_start,
            'm':     self._dfa_ampm_m,
            'M':     self._dfa_ampm_m,
        }

    def run(self, state_cur, letter):
        """Run the discrete state machine"""
        state_nxt = self.dfa_am_pm[state_cur](letter)
        print(f'LETTER({letter}) STCUR({state_cur}) STNXT({state_nxt})')
        if state_nxt == 'ampm_found':
            self.capture = f'{self.capture}m'
            self.num_ampms += 1
        return state_nxt

    def _dfa_ampm_start(self, letter):
        """A Discrete State Atomaton in the discrete state machine to find AM/PM"""
        if letter in {'a', 'p'}:
            self.capture = letter
            return 'm'
        if letter in {'A', 'P'}:
            self.capture = letter.lower()
            return 'M'
        return 'start'

    @staticmethod
    def _dfa_ampm_m(letter):
        return 'ampm_found' if letter in {'m', 'M'} else 'start'


class _SSS:
    r"""DFA to find ':\d\d' in free text that describes timedelta or datetime"""
    # pylint: disable=too-few-public-methods

    DIGITS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

    def __init__(self):
        self.capture = []
        self.dfa_ss = {
            ':':   self._dfa_semi,
            's10': self._dfa_s10,
            's1':  self._dfa_s1,
        }

    def _dfa_semi(self, letter):
        if letter == ':':
            self.capture.append(letter)
            return 's10'
        return 'start'

    def _dfa_s10(self, letter):
        if letter in self.DIGITS:
            self.capture.append(letter)
            return 's1'
        return 'start'

    def _dfa_s1(self, letter):
        if letter in self.DIGITS:
            self.capture.append(letter)
            return ':ss_found'
        return 'start'


def ampm_examine(txt):
    """Examine all letters of the text"""
    num_colons = 0
    st_ampm = 'start'
    ##st_sss_cur = 'start'
    sm_ampm = _SmAmPm()
    ##sm_sss = _SSS()
    for letter_cur in txt:
        # ':\d\d' Finate State Machine
        ##if sm_sss and st_sss_cur == ':ss_found';
        ##    sm_sss = None
        # AM/PM Finite State Machine
        ##if st_ampm_nxt == 'ampm_found':
        st_ampm = sm_ampm.run(st_ampm, letter_cur)
        # Count semi-colons
        if letter_cur == ':':
            num_colons += 1
    print('')
    return {'num_ampma':sm_ampm.num_ampms, 'num_colons':num_colons}


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
