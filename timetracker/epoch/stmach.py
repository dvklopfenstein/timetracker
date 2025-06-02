"""Examine free text representing a timedelta or a datetime"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

DIGITS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

class _Base:
    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.capture = None
        self.state = 'start'
        self.found = False
        self.dfa = None

    def _run(self, state, letter, name, fnc_docapture):
        """Run the discrete state machine to search for pattern"""
        print(f'StateMachine-{name} FOUND({int(self.found)}) LETTER({letter}) '
              f'STCUR({self.state}) STNXT({state})')
        if self.capture is not None and state == 'matched':
            ##self.capture = f'{self.capture}m'
            fnc_docapture()
            self.found = True
        self.state = state
        return state != 'matched'

class _SmAmPm(_Base):
    # pylint: disable=too-few-public-methods

    def __init__(self):
        _Base.__init__(self)
        self.dfa = {
            'start': self._dfa_ampm_start,
            'm':     self._dfa_ampm_m,
            'M':     self._dfa_ampm_m,
        }

    def run(self, letter):
        """Run the discrete state machine to search for pattern"""
        return _Base._run(self, self.dfa[self.state](letter), letter, 'AM/PM', self._do_capture)

    def _do_capture(self):
        self.capture = f'{self.capture}m'

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

    @staticmethod
    def _dfa_ampm_m(letter):
        if letter in {'m', 'M'}:
            return 'matched'
        # Setting capture to None not needed
        return 'start'

class _SDD(_Base):
    r"""DFA to find ':\d\d' in free text that describes timedelta or datetime"""
    # pylint: disable=too-few-public-methods

    def __init__(self):
        _Base.__init__(self)
        self.dfa = {
            'start': self._dfa_semi,
            ':':     self._dfa_semi,
            's10':   self._dfa_s10,
            's1':    self._dfa_s1,
        }

    def run(self, letter):
        """Run the discrete state machine to search for pattern"""
        return _Base._run(self, self.dfa[self.state](letter), letter, ':SS', self._do_capture)

    def _do_capture(self):
        self.capture = ''.join(self.capture)

    def _dfa_semi(self, letter):
        if letter == ':':
            self.capture = [':',]
            return 's10'
        return 'start'

    def _dfa_s10(self, letter):
        if letter in DIGITS:
            self.capture.append(letter)
            return 's1'
        return 'start'

    def _dfa_s1(self, letter):
        if letter in DIGITS:
            self.capture.append(letter)
            return 'matched'
        return 'start'

class _HH(_Base):
    r"""DFA to find \d or \d\d to find the hour"""
    # pylint: disable=too-few-public-methods

    def __init__(self):
        _Base.__init__(self)
        self.dfa = {
            'start': self._dfa_h1,
            'h1':    self._dfa_h2,
        }

    def run(self, letter):
        """Run the discrete state machine to search for pattern"""
        return _Base._run(self, self.dfa[self.state](letter), letter, 'HH', self._do_capture)

    def _do_capture(self):
        self.capture = ''.join(self.capture)

    def _dfa_h1(self, letter):
        if letter in DIGITS:
            self.capture = [letter]
            return 'h1'
        if letter == ':':
            self.state = ':'
            self.found = True
            return 'SS'
        if letter in {'a', 'p'}:
            self.state = 'm'
            self.found = True
            return 'AM'
        if letter in {'A', 'P'}:
            self.state = 'M'
            self.found = True
            return 'AM'
        return 'start'

    def _dfa_h2(self, letter):
        if letter in DIGITS:
            self.capture.append(letter)
            self.found = True
            return 'matched'
        return 'start'


def examine_texttime(txt):
    """Examine all letters of the text"""
    num_colons = 0
    smhh = _HH()
    smmm = _SDD()
    smam = _SmAmPm()
    do_srch = 'HH'
    captures = []
    ### Prepare Search for 'am', 'pm', 'AM', or 'PM'
    ##sm_ampm = _SmAmPm()
    ##search_ampm = True
    ### Prepare Search for seconds in the form of ':\d\d'
    ##sm_sdd = _SDD()
    ##search_sdd = True
    # Search
    for letter_cur in txt:
        if do_srch == 'HH':
            do_srch = smhh.run(letter_cur)
            if smhh.found:
                captures.append(smhh.capture)
        ### ':\d\d' Finate State Machine
        ####if sm_sdd and st_sss_cur == 'matched';
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
