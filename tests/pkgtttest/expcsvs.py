"""Query expected csvs"""

from re import compile as re_compile
from timetracker.csvget import NTCSV


class ExpCsvs:
    """Query expected csvs"""

    FCSV = re_compile(r'home/(?P<username>\w+)/proj/(?P<project>\w+)')

    def __init__(self, orig_ntcsvs, pull_copies):
        self.exp_ntcsvs = orig_ntcsvs + self._init_ntcsvs(pull_copies, orig_ntcsvs)

    def chk_get_csvs_global_all(self, usr2ntcsvs):
        """Check the csvs resulting from `get_csvs_global_uname`"""
        for usr_act, ntcsvs_act in usr2ntcsvs.items():
            ntcsvs_exp = self._exp_get_csvs_global_all(usr_act)
            fcsvs_exp = set(nt.fcsv for nt in ntcsvs_exp)
            fcsvs_act = set(nt.fcsv for nt in ntcsvs_act)
            assert fcsvs_act == fcsvs_exp, self._err(fcsvs_act, fcsvs_exp)
            for ntcsv in ntcsvs_act:
                assert usr_act in ntcsv.fcsv, f'FILE OUTSIDE OF ACCOUNT({usr_act}): {ntcsv.fcsv}'
                #print(f'GLB ALL ACT {usr_act:7} {ntcsv}')

    def chk_get_csvs_global_uname(self, usr2ntcsvs):
        """Check the csvs resulting from `get_csvs_global_uname`"""
        for usr_act, ntcsvs_act in usr2ntcsvs.items():
            ntcsvs_exp = self._exp_get_csvs_global_uname(usr_act)
            assert ntcsvs_act == ntcsvs_exp, self._err(ntcsvs_act, ntcsvs_exp)
            for ntcsv in ntcsvs_act:
                assert ntcsv.username == usr_act
                #print(f'ACT {usr_act:7} {ntcsv}')

    def chk_get_csvs_local_all(self, usrprj2ntcsvs):
        """Check the csvs resulting from `get_csvs_global_uname`"""
        for (usr_act, prj_act), ntcsvs_act in usrprj2ntcsvs.items():
            ntcsvs_exp = self._exp_get_csvs_local_all(usr_act, prj_act)
            fcsvs_exp = set(nt.fcsv for nt in ntcsvs_exp)
            fcsvs_act = set(nt.fcsv for nt in ntcsvs_act)
            assert fcsvs_act == fcsvs_exp, self._err(fcsvs_act, fcsvs_exp)
            for ntcsv in ntcsvs_act:
                assert usr_act in ntcsv.fcsv, f'FILE OUTSIDE OF ACCOUNT({usr_act}): {ntcsv.fcsv}'
                #print(f'GLB ALL ACT {usr_act:7} {ntcsv}')

    def chk_get_csvs_local_uname(self, usrprj2ntcsv):
        """Check the csvs resulting from `get_csvs_global_uname`"""
        for (usr_act, prj_act), ntcsv_act in usrprj2ntcsv.items():
            ntcsv_exp = self._exp_get_csvs_local_uname(usr_act, prj_act)
            assert ntcsv_act == ntcsv_exp, self._err([ntcsv_act], [ntcsv_exp])

    # -------------------------------------------------------------------------------
    def _exp_get_csvs_global_uname(self, uname):
        nts = set()
        for ntcsv in self._exp_get_csvs_global_all(uname):
            if f'_{uname}.csv' in ntcsv.fcsv:
                nts.add(ntcsv)
        return nts

    def _exp_get_csvs_global_all(self, login):
        nts = set()
        for ntcsv in self.exp_ntcsvs:
            if ntcsv.fcsv is not None and f'home/{login}/proj' in ntcsv.fcsv:
                nts.add(ntcsv)
        return nts

    def _exp_get_csvs_local_all(self, login, project):
        nts = set()
        for ntcsv in self.exp_ntcsvs:
            if ntcsv.fcsv is not None and f'home/{login}/proj/{project}' in ntcsv.fcsv:
                nts.add(ntcsv)
        return nts

    def _exp_get_csvs_local_uname(self, login, project):
        for ntcsv in self._exp_get_csvs_local_all(login, project):
            if ntcsv.fcsv is not None and f'_{login}.csv' in ntcsv.fcsv:
                return ntcsv
        return None

    @staticmethod
    def _err(act, exp):
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
