# CHANGELOG

# Summary
* [**Unreleased**](#unreleased)
* [**Release 2025-03-09 v0.3a2**](#release-2025-03-09-v03a3) Added stop --at test; Added report module
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

## Release 2025-03-09 v0.3a3
* ADD stop --at test
* ADD report command
  * Initial implementation works for a single user on a single project (more to come)
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
