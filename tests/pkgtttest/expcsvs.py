"""Query expected csvs"""

from re import compile as re_compile
from timetracker.csvget import NTCSV


class ExpCsvs:
    """Query expected csvs"""

    FCSV = re_compile(r'home/(?P<username>\w+)/proj/(?P<project>\w+)')

    def __init__(self, orig_ntcsvs, pull_copies):
        self.exp_ntcsvs = orig_ntcsvs + self._init_ntcsvs(pull_copies, orig_ntcsvs)

    def chk_get_csvs_global_all(self, key2ntcsvs):
        """Check the csvs resulting from `get_csvs_global_uname`"""
        print(key2ntcsvs)
        for usr_act, ntcsvs_act in key2ntcsvs.items():
            ntcsvs_exp = self._exp_get_csvs_global_all(usr_act)
            fcsvs_exp = set(nt.fcsv for nt in ntcsvs_exp)
            fcsvs_act = set(nt.fcsv for nt in ntcsvs_act)
            assert fcsvs_act == fcsvs_exp, self._err(fcsvs_act, fcsvs_exp)
            for ntcsv in ntcsvs_act:
                assert usr_act in ntcsv.fcsv, f'FILE OUTSIDE OF ACCOUNT({usr_act}): {ntcsv.fcsv}'
                #print(f'GLB ALL ACT {usr_act:7} {ntcsv}')
            print('')

    def chk_get_csvs_global_uname(self, key2ntcsvs):
        """Check the csvs resulting from `get_csvs_global_uname`"""
        print(key2ntcsvs)
        for (usr_act, prj_act), ntcsvs in key2ntcsvs.items():
            self._exp_get_csvs_global_uname(usr_act)
            for ntcsv in ntcsvs:
                print(f'ACT {usr_act:7} {prj_act:11} {ntcsv}')
            print('')

    def _exp_get_csvs_global_uname(self, uname):
        for ntcsv in self.exp_ntcsvs:
            if ntcsv.username == uname:
                print(f'EXP: {uname} {ntcsv}')

    def _exp_get_csvs_global_all(self, login):
        ret = []
        for ntcsv in self.exp_ntcsvs:
            if ntcsv.fcsv is not None and f'home/{login}/proj' in ntcsv.fcsv:
                ret.append(ntcsv)
        return ret

    def _err(self, act, exp):
        errmsg = [f'ACT[{len(act)}] != EXP[{len(exp)}]',]
        errmsg.append('ACT:')
        for idx, elem in enumerate(sorted(act)):
            errmsg.append(f'ACT {idx}) {elem}')
        errmsg.append('EXP:')
        for idx, elem in enumerate(sorted(exp)):
            errmsg.append(f'EXP {idx}) {elem}')
        return '\n'.join(errmsg)

    # -------------------------------------------------------------------------------
    def _init_ntcsvs(self, csv_pull_copies, orig_ntcsvs):
        watchers = set((nt.username, nt.project) for nt in orig_ntcsvs)
        ntcsvs = []
        for fcsv in csv_pull_copies:
            mtch = self.FCSV.search(fcsv)
            assert mtch is not None, 'EXPECTED FILENAME: home/USER/proj/PROJECT'
            username = mtch['username']
            project = mtch['project']
            assert (username, project) in watchers
            ntd = NTCSV(fcsv=fcsv, username=username, project=project)
            ntcsvs.append(ntd)
        return ntcsvs
