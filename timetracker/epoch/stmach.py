"""Examine free text representing a timedelta or a datetime"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"


class _SmAmPm:
    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.capture = None
        self.state = 'start'
        self.dfa_am_pm = {
            'start': self._dfa_ampm_start,
            'm':     self._dfa_ampm_m,
            'M':     self._dfa_ampm_m,
        }

    def run(self, letter):
        """Run the discrete state machine to search for AM/PM"""
        state = self.dfa_am_pm[self.state](letter)
        #print(f'StateMachine-AM/PM LETTER({letter}) STCUR({self.state}) STNXT({state})')
        if self.capture is not None and state == 'ampm_found':
            self.capture = f'{self.capture}m'
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
        # Setting capture to None not needed
        return 'start'

    def _dfa_ampm_m(self, letter):
        if letter in {'m', 'M'}:
            return 'ampm_found'
        # Setting capture to None not needed
        return 'start'


class _SDD:
    r"""DFA to find ':\d\d' in free text that describes timedelta or datetime"""
    # pylint: disable=too-few-public-methods

    DIGITS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

    def __init__(self):
        self.capture = None
        self.state = 'start'
        self.dfa_ss = {
            'start': self._dfa_semi,
            ':':     self._dfa_semi,
            's10':   self._dfa_s10,
            's1':    self._dfa_s1,
        }

    def run(self, letter):
        r"""Run the discrete state machine to search for seconds formatted as ':\d\d'"""
        state = self.dfa_ss[self.state](letter)
        print(f'StateMachine-:dd LETTER({letter}) STCUR({self.state}) STNXT({state})')
        if state == ':ss_found':
            self.capture = ''.join(self.capture)
        self.state = state
        return state != ':ss_found'

    def _dfa_semi(self, letter):
        if letter == ':':
            self.capture = [':',]
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
    ### Prepare Search for 'am', 'pm', 'AM', or 'PM'
    ##sm_ampm = _SmAmPm()
    ##search_ampm = True
    ### Prepare Search for seconds in the form of ':\d\d'
    ##sm_sdd = _SDD()
    ##search_sdd = True
    # Search
    for letter_cur in txt:
        ### ':\d\d' Finate State Machine
        ####if sm_sdd and st_sss_cur == ':ss_found';
        ####    sm_sdd = None
        ### AM/PM Finite State Machine
        ##if search_ampm:
        ##    search_ampm = sm_ampm.run(letter_cur)
        ##if search_sdd:
        ##    search_sdd = sm_add.run(letter_cur)
        # Count semi-colons
        if letter_cur == ':':
            num_colons += 1
    ##return {'num_ampma':sm_ampm.num_ampms, 'num_colons':num_colons}


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
