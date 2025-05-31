"""Examine free text representing a timedelta or a datetime"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"


class _SmAmPm:
    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.capture = None
        self.state = 'start'
        self.num_ampms = 0
        self.dfa_am_pm = {
            'start': self._dfa_ampm_start,
            'm':     self._dfa_ampm_m,
            'M':     self._dfa_ampm_m,
        }

    def run(self, letter):
        """Run the discrete state machine"""
        state = self.dfa_am_pm[self.state](letter)
        print(f'StateMachine-AM/PM LETTER({letter}) STCUR({self.state}) STNXT({state})')
        if self.capture is not None and state == 'ampm_found':
            self.capture = f'{self.capture}m'
            self.num_ampms += 1
        self.state = state
        return state != 'ampm_found'

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


class _SDD:
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
    search_ampm = True
    #search_sdd = True
    ##st_sss_cur = 'start'
    sm_ampm = _SmAmPm()
    #sm_sdd = _SDD()
    for letter_cur in txt:
        # ':\d\d' Finate State Machine
        ##if sm_sdd and st_sss_cur == ':ss_found';
        ##    sm_sdd = None
        # AM/PM Finite State Machine
        if search_ampm:
            search_ampm = sm_ampm.run(letter_cur)
        #if search_sdd:
        #    search_sdd = sm_add.run(letter_cur)
        # Count semi-colons
        if letter_cur == ':':
            num_colons += 1
    return {'num_ampma':sm_ampm.num_ampms, 'num_colons':num_colons}


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
