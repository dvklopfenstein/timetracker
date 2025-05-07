<!--
Copyright (C) DV Klopfenstein, PhD
License: https://www.gnu.org/licenses/agpl-3.0.en.html#license-text
https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup
-->
# The global timetracker config file
The global configuration file contains a list of all projects (repos) managed by timetracker.
A project is added to the global configuration file by the `init` command.
The timetracker-csv `export` command concatenates CSV files for each repo into a single CSV file for multi-project analysis.
Commands such as `hours` and `report` use the global config
if the researcher asks for total hours for multiple projects.

* [Location](#location)

## Location
1. `~/.timetrackerconfig`: Contains a list of projects time-tracked specifically by you.

2. The environmental variable, `TIMETRACKERCONF` may be used to specify
a global timetracker-csv file other than  '~/.timetrackerconfig'.

3. The timetracker-csv global config file can be specified on the command-line at runtime.
Specifying the global config file on the CLI overrides using '~/.timetrackerconfig' or 
the config file specified by `TIMETRACKERCONF`.

Copyright (C) 2025, DV Klopfenstein, PhD. All rights reserved
