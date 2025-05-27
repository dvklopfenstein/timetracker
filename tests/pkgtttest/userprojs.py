"""Manage user projects"""

from os.path import join
from collections import defaultdict
from timetracker.csvget import NTCSV

# USERPROJS EXAMPLE:
#
# userprojs = {
#     ('david'  , 'shepherding'): ([('Sun', 'Fri', '5am', '11:30pm')], 111.0),
#     ('david'  , 'sleeping'):    ([],   0.0),
#     ('david'  , 'grazing'):     ([],   0.0),
#     ('david'  , 'hunting'):     ([],   0.0),
#
#     ('lambs'  , 'sleeping'):    ([('Mon', 'Sat',  '7pm',   '11pm')],  24.0),
#     ('lambs'  , 'grazing'):     ([('Mon', 'Sat',  '6am',    '8am'),
#                                   ('Mon', 'Sat',  '9am',   '10am'),
#                                   ('Mon', 'Sat', '11am',   '12pm'),
#                                   ('Mon', 'Sat',  '2am',    '3pm'),
#                                   ('Mon', 'Sat', ' 7pm',    '8pm')], 108.0),
#     ('goats'  , 'sleeping'):    ([('Mon', 'Sat',  '6:59pm', '11:59pm')], 30.0),  # 3
#     ('goats'  , 'grazing'):     ([('Wed', 'Fri', '10am',    '4pm')],  18.0),
#
#     ('lions'  , 'hunting'):     ([('Mon', 'Fri',  '7pm',    '8pm')],   5.0),
#     ('lions'  , 'sleeping'):    ([],   0.0),
#     ('lions'  , 'grazing'):     ([],   0.0),
#     ('lions'  , 'shepherding'): ([],   0.0),
#     ##('jackels', 'scavenging'):  ([('Sun', 'Fri',  '9am',    '3pm')],  36.0),
# }

class UserProjects:
    """Manage user projects"""

    def __init__(self, userprojs):
        self.userprojs = userprojs
        self.usernames = self._init_users()
        self.project = self._init_projects()

    def get_expcsvs(self, tmproot):
        """Get the expected csv filenames"""
        ret = []
        for (usr, prj), (times, exphours) in self.userprojs.items():
            assert exphours is not None, f'{usr} {prj}: {exphours} {times}'
            csv = None
            if times:
                csv = f'timetracker_{prj}_{usr}.csv'
                csv = join(tmproot, 'home', usr, 'proj', prj, csv)
            ret.append(NTCSV(
                fcsv=csv,
                project=prj,
                username=usr))
        return ret

    def get_usr2projects(self):
        """Get all projects for a single user"""
        usr2projects = defaultdict(set)
        for (usr, prj) in self.userprojs:
            usr2projects[usr].add(prj)
        return dict(usr2projects)

    def get_usr2configs(self, tmproot):
        """Get all NtCsv items for each user"""
        usr2configs = defaultdict(set)
        for usr, projects in self.get_usr2projects():
            for prj in projects:
                usr2configs[usr].add(join(tmproot, usr, 'proj', prj, '.timetracker/config'))
        return dict(usr2configs)

    def get_configs(self, tmproot):
        """Get expected local project config files"""
        cfgs = set()
        for usr, projects in self.get_usr2projects():
            for prj in projects:
                cfgs.add(join(tmproot, usr, 'proj', prj, '.timetracker/config'))
        return cfgs

    # -----------------------------------------------------------
    def _init_users(self):
        """Get the set of all users"""
        return sorted(set(usr for (usr, prj) in self.userprojs))

    def _init_projects(self):
        """Get the set of all users"""
        return sorted(set(prj for (usr, prj) in self.userprojs))
