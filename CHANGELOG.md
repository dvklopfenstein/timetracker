# CHANGELOG

# Summary
* [**Unreleased**](#unreleased)
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
