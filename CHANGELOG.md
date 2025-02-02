# CHANGELOG

# Summary
* [**Unreleased**](#unreleased)
* [**Release 2025-02-02 v0.1a4**](#release-2025-02-02-v01a4) Added global config file
* [**Release 2025-01-27 v0.1a3**](#release-2025-01-27-v01a3) Added local config; enables researcher to set csv location
* [**Release 2025-01-22 v0.1a2**](#release-2025-01-22-v01a2) Install with `pip install timetracker-csv`
* [**Release 2025-01-22 v0.1a1**](#release-2025-01-22-v01a1) Initial implementation of cmds: init, start, and stop


# Details

## Unreleased

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
