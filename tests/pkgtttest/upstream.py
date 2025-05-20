"""Mock Upstream git-like object"""

from os import makedirs
from os.path import exists
from os.path import relpath
from os.path import join
from os.path import dirname
from shutil import copy
from filecmp import cmp
from tests.pkgtttest.mkprojs import get_files

class Upstream:
    """Mock Upstream git-like object"""

    def __init__(self, dirupstream):
        self.dirupstream = dirupstream
        makedirs(dirupstream, exist_ok=True)
        #self.nto = namedtuple('NtFile'
        self.proj2obj = {}

    def prt_files(self):
        """Print the files in upstream"""
        files = get_files(self.dirupstream)
        print(f'\nFILES[{len(files)}] IN UPSTREAM {self.dirupstream}:')
        for fname in files:
            print(fname)

    def pull(self, project, diruser):
        """Mimic a git 'pull' for a file"""
        if project not in self.proj2obj:
            return None
        updir = self._get_project_dir(project)
        files = get_files(updir)
        copies = []
        for repo_absfilename in files:
            repo_relfilename = relpath(repo_absfilename, updir)
            user_absfilename = join(diruser, repo_relfilename)
            if not exists(user_absfilename):
                makedirs(dirname(user_absfilename), exist_ok=True)
                print(f'copy({repo_absfilename}, {user_absfilename}')
                copy(repo_absfilename, user_absfilename)
                copies.append(user_absfilename)
            else:
                assert cmp(repo_absfilename, user_absfilename)
        return copies

    def push(self, project, absfilename, relfilename):
        """Add/update and upstream project and 'push' a file"""
        if project not in self.proj2obj:
            makedirs(join(self.dirupstream, project), exist_ok=True)
            self.proj2obj[project] = set()
            self._add_file(project, absfilename, relfilename)
            return
        if relfilename in self.proj2obj[project]:
            if cmp(absfilename, self._get_fname_upstream(project, relfilename)):
                return
            self.prt_files()
            raise RuntimeError(f'FILE NOT MATCH: {project}: {relfilename}')
        self._add_file(project, absfilename, relfilename)

    def _add_file(self, project, absfilename, relfilename):
        dst = self._get_fname_upstream(project, relfilename)
        makedirs(dirname(dst), exist_ok=True)
        copy(absfilename, dst)
        self.proj2obj[project].add(relfilename)

    def _get_fname_upstream(self, project, relfilename):
        return join(self.dirupstream, project, relfilename)

    def _get_project_dir(self, project):
        return join(self.dirupstream, project)
