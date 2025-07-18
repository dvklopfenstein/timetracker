# CHANGELOG

# Summary
* [**Unreleased**](#unreleased)
* [**Release 2025-07-15 v0.8a4**](#release-2025-07-15-v08a4) Made options and output more concise
* **Release 2025-07-04 v0.8.3** Clean README
* [**Release 2025-06-28 v0.8a1**](#release-2025-06-28-v08a1) Added the command `trk running`
* [**Release 2025-06-28 v0.8a0**](#release-2025-06-28-v08a0) Documentation; minor speed; simplify stop defaults
* [**Release 2025-06-21 v0.7a0**](#release-2025-06-21-v07a0) Much added functionality for invoicing
* [**Release 2025-05-27 v0.6a0**](#release-2025-05-27-v06a0) Added functions to collect various groups of csv files
* [**Release 2025-05-18 v0.5a7**](#release-2025-05-18-v05a7) Add starttime to `report`; Bug fix in `cancel`
* [**Release 2025-05-16 v0.5a6**](#release-2025-05-16-v05a6) Add options to `projects` command; Fix `report` command
* [**Release 2025-05-15 v0.5a5**](#release-2025-05-15-v05a5) Report command tested and updated; Get csv files for a single user tested and implemented
* **Release 2025-05-14 v0.5a4** Optimized getting csv files to report locally or globally for a single user
* **Release 2025-05-08 v0.5a3** Add all timetracker packages
* **Release 2025-05-07 v0.5a2** Use pyproject.toml rather than setup.py
* [**Release 2025-05-02 v0.5a1**](#release-2025-05-02-v05a1) Fixed bug when forcing a new csv filename in reinit
* [**Release 2025-04-30 v0.5a0**](#release-2025-04-30-v05a0) New command function: projects, hours; began docs
* [**Release 2025-03-21 v0.4a0**](#release-2025-03-21-v04a0) Added prerequisite, dateparser, to replace dateutil
* [**Release 2025-03-18 v0.3a8**](#release-2025-03-18-v03a8) Added `--activity` & `--tags` option to `stop' command; Use new concise csv
* [**Release 2025-03-14 v0.3a4**](#release-2025-03-14-v03a4) Added stop --at test; Added report module
* [**Release 2025-02-25 v0.3a0**](#release-2025-02-25-v03a0) Added --at functionality to start & stop command
* **Release 2025-02-18 v0.2a5** Changed logo to a stopwatch
* **Release 2025-02-18 v0.2a4** Added `trk time` command to report elapsed hours
* [**Release 2025-02-15 v0.2a3**](#release-2025-02-15-v02a3) Implemented functionality & Wrote tests for csv management
* **Release 2025-02-08 v0.2a1** Cleaned up tests; Added pytest to GitHub workflows upon push
* **Release 2025-02-07 v0.2a0** Added functionality for running in project subdirs
* [**Release 2025-02-05 v0.1a8**](#release-2025-02-05-v01a8) Added DOI for citing
* [**Release 2025-02-02 v0.1a4**](#release-2025-02-02-v01a4) Added global config file
* [**Release 2025-01-27 v0.1a3**](#release-2025-01-27-v01a3) Added local config; enables researcher to set csv location
* [**Release 2025-01-22 v0.1a2**](#release-2025-01-22-v01a2) Install with `pip install timetracker-csv`
* [**Release 2025-01-22 v0.1a1**](#release-2025-01-22-v01a1) Initial implementation of cmds: init, start, and stop


# Details

## Unreleased

## Release 2025-07-15 v0.8a4
* CHANGED `trk running` output to be more concise
* ADDED short option '-d' to original long option '--csvdir' in command, 'trk init'
* ADDED new script, `timecalc` that takes two of: starttime, stoptime, or timedelta and
  returns the missing datetime or timedelta
* ADDED documentation for `trk running`

## Release 2025-06-28 v0.8a1 - 2025-07-04 v0.8a3
* CHANGED: README cleanup and added links

## Release 2025-06-28 v0.8a1
* ADDED command, `trk running` and `trk running --verbose`

## Release 2025-06-28 v0.8a0
* CHANGED Starttime object for minor import speed improvement
* CHANGED `trk stop -m msg` message be specified on command line

## Release 2025-06-21 v0.7a0
* ADDED command, `trk invoice`
* ADDED command option, `-b` or `--billable` to `trk stop`
  to add a `Billable` tag when running `tag stop`
* ADDED command, `trk paid`; `Billable` tag is added so the amount paid
  will be printed in the invoice
* ADDED `trk stop -b` or `trk stop --billable` to add 'Billable' tag with minimum typing
* ADDED `--no-git-add` and `-A` options to the `trk init` command
* CHANGED speed to 100x faster for parsing free text into datetime objects
* CHANGED "Run `trk init`" message so it is clearer that no trk command
  will be run until the project is initialized
* CHANGED imports to improve speed

## Release 2025-05-27 v0.6a0
* ADDED `trk hours` options `--global` to show hours for all projects for a single username
* ADDED `trk hours` options `--global` `--all-users` for hours for all projects for all usernames
* ADDED function get_csv_local_uname
* ADDED function get_csvs_local_all
* ADDED function get_csvs_global_uname
* ADDED function get_csvs_global_all
* ADDED running `git add .timetracker/config .timetracker/.gitignore` during initialization
* FIXED exit gracefully if `start --at` datetime cannot be parsed

## Release 2025-05-18 v0.5a7
* ADDED start time to `report` stdout
* FIXED incorrect param order in `cancel`

## Release 2025-05-16 v0.5a6
* ADDED `trk project` option, `--exists` to mark which projects exist
* ADDED `trk project` option, `--rm-missing` to
         remove projects that do not exist from the list in the global config
* FIXED `trk report` by removing an obsolete param

## Release 2025-05-15 v0.5a5
* ADDED Add functions (and tests) to get local project csvs
* ADDED Add test for the report command
* CHANGED Optimize the report command
* CHANGED Move stdout messages to the common command module from the starttime class
* CHANGED Get workflows upon push working again

## Release 2025-05-02 v0.5a1
* CHANGED local project config user message to print current csv filename 

## Release 2025-04-21 v0.5a0
* ADDED `projects` command to get a list of projects
* ADDED ability to specify the global config file from the cli
* ADDED writing the name of the global config file into the project config file,
        if given on the command line
* ADDED option for getting global config file from local config file (function: get_filename_globalcfg)
* ADDED major documentation start
* ADDED a new console script, `timestr`, to test how time strings are converted to `datetime` by `dateparser`
* ADDED reinitialization command using `trk init --force`
* ADDED issue tracker
* ADDED csv converter to convert original format to more concise format
* ADDED `trk stop -m d` will use your last git commit message as the timetracker stop message
* ADDED new `epoch` package to manage all time modules
* ADDED two new test scripts to test how time strings are converted to `datetime` objects by `dateparser` and `dateutils`
* CHANGED command name `time` to `hours`
* CHANGED to using EAFP (Easier To Ask For Permission) when reading cfgs and csvs

## Release 2025-03-21 v0.4a0
* ADD new prerequisite, dateparser, due to its accuracy and flexibility
* REMOVE prerequisite, dateutil, due to its incorrect output and lack of flexibility
  https://github.com/dateutil/dateutil/issues/1421

## Release 2025-03-18 v0.3a8
* ADD `convert_csv` function to convert old csv format to new concise csv format
* ADD to `stop` command: `--activity` and `--tags` options
* CHANGE data format in csv to be more readable and require less disk space
  * ADD converter to convert csv's using the old format to the new format

## Release 2025-03-14 v0.3a4
* ADD stop --at test
* ADD report command
  * Initial implementation works for a single user on a single project (more to come)
* CHANGED arg, `--trksubdir` to `--trk-dir` to match git's `--git-dir`
* CHANGED CfgGlobal param to the config filename
* CHANGED code to use [pytimeparse2](https://github.com/onegreyonewhite/pytimeparse2)
          before dateutils to 
          ensure stopping the timer in "4hours"
          is interpreted as "4hours from now" and
          not "4am today" https://github.com/dateutil/dateutil/issues/1421
* CHANGED code to adapt to dateutils parse function behavior
* CHANGED Fine-tuned stdout messages to researcher for commands: start, stop, and cancel
* CHANGED datetime & timedelta parsing to be simpler
* CHANGED to ensure None is written as '' in csv
* CHANGED csv writing code from the stop command to the CsvFile object

## Release 2025-02-25 v0.3a0
* ADD `--at` and `--force` to `start` and `stop` commands
* ADD cancel command

## Release 2025-02-15 v0.2a3
* ADD Test for csv management
* ADD Finder function, get_dircsv_default, for printing in CLI help messages
* ADD csv-finding functionality
* CHANGE Starttime to its own module
  * ADD CfgProj function to get Starttime instance

## Release 2025-02-05 v0.1a8
* ADD: Zenodo citation and CITATION.cff file
* ADD: Finder, which finds a timetracker config file in the current or parent dirs
* ADD: pyproject.toml file
* CHANGE: Streamline architecture

## Release 2025-02-02 v0.1a4
* ADD: Global cfg parser
* ADD: `--version` arg
* ADD: `trk init --project PROJECT` for a researcher-specified project username
* ADD: If global cfgfilename is a parent of project cfgfilename,
       write `~/pathtoproj/.timetracker/config' in global cfg
* ADD: Logo to README.md; Currently is `work under progress`
* ADD: Now can specify a local project test working dir other than `./.timetracker` using `-d` or `--trksubdir`

## Release 2025-01-27 v0.1a3
* CHANGED: Executable name from `trkr` to the shorter `trk`
* ADD: Local project Configuration parser
* ADD: Local project cfg parser is written upon init, with --csvdir setting csv file location
* ADD: Local project cfg parser is read upon `trkr stop -m msg`; time written to csv file in researcher-specied location

## Release 2025-01-22 v0.1a2
* ADD: Install with `pip install timetracker-csv`

## Release 2025-01-22 v0.1a1
This is a 
[Technical Preview (a)](https://github.blog/changelog/2024-10-18-new-terminology-for-github-previews/)
release to be used for research projects.
Note that `a` must be used in pre-release version identifiers
because pip does not currently support
`tp` for the "Technical Preview" project stage.
* Determine and implement architecture
* ADD cli commands:
  * `init`  -- Currently creates the local .timetracker/ directory
  * `start` -- Starts the timer
  * `stop`  -- Stops the timer; Records in a timetracker csv
