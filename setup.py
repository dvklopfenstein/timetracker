"""For building and installing TimeTracker"""

from setuptools import setup
from os.path import join

PACKAGES = [
    'timetracker',
]

PACKAGE_DIRS = {p:join(*p.split('.')) for p in PACKAGES}
print(PACKAGE_DIRS)

CONSOLE_SCRIPTS = [
    'timetracker=timetracker.cli:main',
]

setup(
    name='timetracker',
    version='0.0.1',
    author='DV Klopfenstein, PhD',
    author_email='dvklopfenstein@protonmail.com',
    packages=PACKAGES,
    package_dir=PACKAGE_DIRS,
    entry_points={
        'console_scripts': CONSOLE_SCRIPTS,
    },
    # https://pypi.org/classifiers/
    classifiers=[
        'Programming Language :: Python',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
    ],
    url='http://github.com/dvklopfenstein/timetracking',
    description="Command-line timetracker that stores data in csv files",
)
