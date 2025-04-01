<!--
Copyright (C) DV Klopfenstein, PhD
License: https://www.gnu.org/licenses/agpl-3.0.en.html#license-text
-->

# Overview
`trk` is a simple [pandas](https://pandas.pydata.org/pandas-docs/stable/index.html)-friendly 
timetracking application for the command line.

You can use it to swiftly create, report, analyze, and plot time units.
Time is stored in pandas-friendly human-readable 
[plain-text](https://lifehacker.com/i-still-use-plain-text-for-everything-and-i-love-it-1758380840)
CSV files.


## Comma separated values
`trk` stores each time unit in plain text in comma separated values (CSV) files.
`trk` CSV files can be stored anywhere,
including git-managed repos stored on GitHub,
dropbox folders, or
encrypted [proton-drive](https://proton.me/drive) folders.
[Proton](https://proton.me/) is a "privacy by default" encrypted suite of tools, including email,
that over 100 million people use to stay private and secure online.

Comma-separated files contain tables (rows and columns) of data and
can be opened using popular editors such as
vim, emacs, or notepad++.
They can also be opened Excel.

## Tags
To analyze groups of time entries later,
`trk` includes support for tags,
which are stored in their own column in the CSV files.
You can find and filter entries by using tags
along with other search conditions using pandas.
Tags are stored in the last column of the `trk` CSV files.
Multiple tags are separated by the `;` character.

## Activities
Each CSV files contains a column that can optionally contain an activity.
Activities can streamline analyzing and plotting groups of time slots.


## Support for multiple projects
`trk` supports multiple projects.
Each project can be maintained as a `git`-managed `repo` (repository). 
Git is a popular version control system used by millions
to ensure that none of their work is lost and that
collaborators can work together seamlessly on a single project
with minimal conflicts,
even if they are working on the same file at the same time.
In a project managed by git,
each person works without anyone hoovering over their shoulder
or deleting their edits as they add them,
as can occur with tools such as Google docs.
Once a researcher is happy with their edits,
they can share them with fellow collaborators
by doing a "Pull Request" or `PR` as the cool kids say.

`trk` is intended to work in a git repo 
containing a project developed by multiple researchers.
The project time for each researcher is stored
in one CSV file per researcher.
This ensures that there are no conflicts in the CSV files
as multiple researchers work on the same project at the same time.

The project CSV files can be stored
within the git-managed project or
outside of the project directory.
The location of the projct CSV files
is set when time tracking is initialized
within the repo using `trk init --csvdir`.
If the `--csvdir` is ommitted,
the CSV files are stored in the root directory of the project repo.
An example of initializing `trk` to store store
CSV files within a project subdirectory is:
`trk init --csvdir doc/timetracking/`.
The subdirectory `doc/timetracking/` must be created by the researcher,
which is commonly done with `mkdir -p doc/timetracking`.
The CSV files can be hand-edited, if desired by a researcher.

## export
Multiple CSV files are concatenated (strung together one by one)
into a single CSV file using the `trk export` command.

## Multi-platform support
`trk` is compatible with most operating systems.
You can [download](./installation.md) it using pip,
the package manager for Python packages
or you can build from a cloned repo.

## Libre software and open-source
`trk` is written in [Python](https://www.python.org).
Ideas and inspirations are [heartily welcome](https://github.com/dvklopfenstein/timetracker/issues/new/choose).

Copyright (C) 2025, DV Klopfenstein, PhD. All rights reserved
