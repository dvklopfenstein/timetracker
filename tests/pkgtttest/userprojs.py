"""Manage user projects"""

from os.path import join
from collections import defaultdict
#from timetracker.csvget import NTCSV


class UserProjects:
    """Manage user projects"""

    def __init__(self, userprojs):
        self.userprojs = userprojs
        self.usernames = self._init_users()
        self.project = self._init_projects()

    def get_usr2projects(self):
        """Get all projects for a single user"""
        usr2projects = defaultdict(set)
        for (usr, prj) in self.userprojs:
            usr2projects[usr].add(prj)
        return dict(usr2projects)

    def get_usr2configs(self, dirhome):
        """Get all NtCsv items for each user"""
        usr2configs = defaultdict(set)
        for usr, projects in self.get_usr2projects():
            for prj in projects:
                usr2configs[usr].add(join(dirhome, usr, 'proj', prj, '.timetracker/config'))
        return dict(usr2configs)

    def get_configs(self, dirhome):
        """Get expected local project config files"""
        cfgs = set()
        for usr, projects in self.get_usr2projects():
            for prj in projects:
                cfgs.add(join(dirhome, usr, 'proj', prj, '.timetracker/config'))
        return cfgs

    # -----------------------------------------------------------
    def _init_users(self):
        """Get the set of all users"""
        return sorted(set(usr for (usr, prj) in self.userprojs))

    def _init_projects(self):
        """Get the set of all users"""
        return sorted(set(prj for (usr, prj) in self.userprojs))
