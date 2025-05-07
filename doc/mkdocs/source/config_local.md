<!--
Copyright (C) DV Klopfenstein, PhD
License: https://www.gnu.org/licenses/agpl-3.0.en.html#license-text
https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup
-->
# The local (project) timetracker config file(s)
The local configuration file the project name and a pattern for the csv filename where time units are appended upon running `trk stop`..
A project is added to the local configuration file by the `init` command.
The timetracker-csv `export` command concatenates CSV files for each repo into a single CSV file for multi-project analysis.
Commands such as `hours` and `report` use the local config
if the researcher asks for total hours for multiple projects.

* [Location](#location)

## Location
1. `~/.timetrackerconfig`: Contains a list of projects time-tracked specifically by you.

2. The environmental variable, `TIMETRACKERCONF` may be used to specify
a local timetracker-csv file other than  '~/.timetrackerconfig'.

3. The timetracker-csv local config file can be specified on the command-line at runtime.
Specifying the local config file on the CLI overrides using '~/.timetrackerconfig' or 
the config file specified by `TIMETRACKERCONF`.

## Examples

### Initialize a timetracker project repo
#### The sheep decide to start a new project called `grazing`.
```
# Version-manage the grazing project:
$ cd /home/sheep/projects/
$ git init grazing
Initialized empty Git repository in /home/sheep/projects/grazing/grazing/.git/

# Time-track the grazing project:
$ trk init
Initialized timetracker directory:  /home/sheep/projects/grazing/grazing/.timetracker

### Example of using multiple local config files
The sheep and the goats begin to track their time grazing.

The lions and the wolves want to observe the sheep and the goats,
but do not want the sheep and goats to know.
So they begin tracking their time on the hunting project.

David is taking care of the herds and flocks by
watching over his flock and being on the lookout for lions.

Copyright (C) 2025, DV Klopfenstein, PhD. All rights reserved
