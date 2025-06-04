"""Examine free text representing a timedelta or a datetime"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

DIGITS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

class _Base:
    # pylint: disable=too-few-public-methods

    def __init__(self, name):
        self.name = name
        self.capture = None
        self.state = 'start'
        self.found = False
        self.advance = False
        self.dfa = None

    def _run(self, state, letter, fnc_docapture):
        """Run the discrete state machine to search for pattern"""
        print(f'StateMachine-{self.name} FOUND({int(self.found)}) LETTER({letter}) '
              f'STCUR({self.state}) STNXT({state})')
        if self.capture is not None and state == 'matched':
            ##self.capture = f'{self.capture}m'
            fnc_docapture()
            self.found = True
        self.state = state
        return state != 'matched'

    def __str__(self):
        return f'{self.name} {int(self.found)} ST({self.state}) {self.capture}'

class _SmAmPm(_Base):
    # pylint: disable=too-few-public-methods

    def __init__(self):
        _Base.__init__(self, 'AM')
        self.dfa = {
            'start': self._dfa_ampm_start,
            'm':     self._dfa_ampm_m,
            'M':     self._dfa_ampm_m,
        }

    def run(self, letter):
        """Run the discrete state machine to search for pattern"""
        return _Base._run(self, self.dfa[self.state](letter), letter, self._do_capture)

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
        _Base.__init__(self, 'SS')
        self.dfa = {
            'start': self._dfa_semi,
            ':':     self._dfa_semi,
            's10':   self._dfa_s10,
            's1':    self._dfa_s1,
        }

    def run(self, letter):
        """Run the discrete state machine to search for pattern"""
        return _Base._run(self, self.dfa[self.state](letter), letter, self._do_capture)

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
        _Base.__init__(self, 'HH')
        self.dfa = {
            'start': self._dfa_h1,
            'h1':    self._dfa_h2,
            'h2':    self._nxt_sm,
        }

    def run(self, letter):
        """Run the discrete state machine to search for pattern"""
        return _Base._run(self, self.dfa[self.state](letter), letter, self._do_capture)

    def _do_capture(self):
        self.capture = ''.join(self.capture)

    def _dfa_h1(self, letter):
        if letter in DIGITS:
            self.capture = [letter]
            return 'h1'
        return 'start'
        #return self._dfa_nxtsm(letter)

    def _dfa_h2(self, letter):
        if letter in DIGITS:
            self.capture.append(letter)
            self.found = True
            return 'h2'
        return self._nxt_sm(letter)

    def _nxt_sm(self, letter):
        if letter == ':':
            self.state = ':'
            self.found = True
            self.advance = 1
            return 'SS'
        if letter in {'a', 'p'}:
            self.state = 'm'
            self.found = True
            self.advance = 2
            return 'AM'
        if letter in {'A', 'P'}:
            self.state = 'M'
            self.found = True
            self.advance = 2
            return 'AM'
        return 'start'


def examine_texttime(txt):
    """Examine all letters of the text"""
    num_colons = 0
    it_hhss = iter([_HH(), _SDD(), _SmAmPm()])
    smo = next(it_hhss)
    captures = []
    ### Prepare Search for 'am', 'pm', 'AM', or 'PM'
    ##sm_ampm = _SmAmPm()
    ##search_ampm = True
    ### Prepare Search for seconds in the form of ':\d\d'
    ##sm_sdd = _SDD()
    ##search_sdd = True
    # Search
    for letter_cur in txt:
        if smo is not None:
            print(smo.run(letter_cur))
            ##if not smo.run(letter_cur):
            ##    try:
            ##        smo = next(it_hhss)
            ##    except StopIteration:
            ##        smo = None
            print(f'XXXXXXXXXXXXXXXXXXXXXX {letter_cur} {smo}\n')
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
    print(f'StateMachine: captures={captures}')
    ##return {'num_ampma':sm_ampm.num_ampms, 'num_colons':num_colons}


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
