# Timetracker-csv
[![PyPI - Version](https://img.shields.io/pypi/v/timetracker-csv)](https://pypi.org/project/timetracker-csv)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14803225.svg)](https://doi.org/10.5281/zenodo.14803225)
![GitHub License](https://img.shields.io/github/license/dvklopfenstein/timetracker)

Track time spent on multiple projects,
one repo at a time from the [CLI](https://blog.iron.io/pros-and-cons-of-a-command-line-interface)    

Time is saved in
[pandas](https://pandas.pydata.org/pandas-docs/stable/index.html)-friendly
[csv](https://www.datarisy.com/blog/understanding-csv-files-use-cases-benefits-and-limitations) files

<p align="center"><img src="https://github.com/dvklopfenstein/timetracker/raw/main/docs/images/stopwatch.png" alt="timetracker" width="750"/></p>

* [Advantages](#advantages)
* [Quickstart](#quickstart)
* [Installation](#installation)
* [Other time-trackers](#other-timetrackers)
* [Issues and feedback](https://github.com/dvklopfenstein/timetracker/issues/new/choose)

## Documentation
* [**QUICKSTART**](quickstart.md)
* [**OVERVIEW**](overview.md)
* **USERGUIDE**
  * [Installation](installation.md)
* [**CONTRIBUTING**](contributing.md)


## Advantages
* Libre Software (aka open-source)
* Quick to set up
* Own your data
* NO invasive tracking **ever** of (as is done by multitudinous other timetracking apps):
* Human-readable ASCII data stored in csv (comma-separated values) [plaintext](http://www.markwk.com/plain-text-life.html) files:
  * Ready for [pandas](https://pandas.pydata.org/), the prevailing Python Data Analysis Library
  * Editable using [many editors](https://survey.stackoverflow.co/2024/technology/#3-integrated-development-environment), including vim and Notepad++
* Modify your data if you forget to log time
* Quickly see the current task being recorded
* Quickly see elapsed time spent on the current task
* No clicking and clicking and clicking on a GUI
* No required use of the internet or cloud-based services
* Data supported for each time interval includes:
  * A required free-form descriptive message
  * An optional `activity` or type
  * Any number of tags
* Export data for import by external time-tracking viewers

## Quickstart
The `name` used by this time tracker is determined by the `USER` environmental variable by default.
### 1) Initialize a timetracker project
```
$ trk init
Initialized timetracker directory: /PROJDIR/.timetracker
```
### 2) Start the timer
```
$ trk start
Timetracker started now: Mon 09:00 AM: 2025-03-24 09:00:00
```
### 3) Stop the timer
```
$ trk stop -m 'Accomplished the planned task'
Timer stopped at Mon 2025-03-24 12:00:00 PM
Elapsed H:M:S 0:03:00 appended to timetracker_timetracker_dvk.csv
```
### 4) Report my time units for this project
```
$ trk report
Day  Date        Span     Total  Description
Sun  2025-03-24  03:00    03:00  Accomplished the planned task
```
You can also get the total hours that you spent on a project:
```
$ trk hours
0:03:00 H:M:S or 3.000 hours
```

## Installation
Install with [timetracker-csv](https://pypi.org/project/timetracker-csv/) pip:
```
$ pip install timetracker-csv
```
Or install from source:
```
$ git clone git@github.com:dvklopfenstein/timetracker.git
$ cd timetracker
$ pip install .
```

[pages](http:/dvklopfenstein.github.io/timetracker)

Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved
