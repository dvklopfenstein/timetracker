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
* [Documentation](docs/README.md)
* [Issues and feedback](https://github.com/dvklopfenstein/timetracker/issues/new/choose)

## Advantages
* Freedom Software (aka open-source)
* Quick to set up
* Own your data
* NO invasive tracking **ever** of (as is done by multitudinous other timetracking apps):
  * keyboard and mouse activity
  * currently active browser tab and its title and URL
  * currently active application and the title of its window
* Human-readable ASCII data stored in csv (comma-separated values) [plaintext](http://www.markwk.com/plain-text-life.html) files:
  * Ready for [pandas](https://pandas.pydata.org/), a prevailing Python Data Analysis Library
  * Editable using [many editors](https://survey.stackoverflow.co/2024/technology/#3-integrated-development-environment), including vim and Notepad++
* Modify your data if you forget to log time
* Quickly see the current task being recorded
* Quickly see elapsed time spent on the current task
* No clicking and clicking and clicking on a GUI
* No required use of the internet or cloud-based services
* Data supported for each time interval includes:
  * A required free-form descriptive message
  * An optional `activity` or `type`
  * Any number of tags
* Plans to support exporting data for import by external time-tracking viewers

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

## Other timetrackers
* 700+ stars [Bartib](https://github.com/nikolassv/bartib)
* 740+ stars [timetrace](https://github.com/dominikbraun/timetrace)
* 13k stars [ActivityWatch](https://github.com/ActivityWatch/activitywatch)
* 85 stars [ti](https://github.com/richmeta/ti)
* 44 stars [tim](https://github.com/MatthiasKauer/tim)
* 6 stars [Jupyter timetracker](https://github.com/PrateekKumarPython/jupyter-timetracker) uses aTimeLogger csv format
* https://atimelogger.pro/ csv files
* [List of timetrackers in PyPi](https://pypi.org/search/?q=timetracker)
* [web-based time tracking application](https://github.com/anuko/timetracker)
* [Wage Labor record](https://pypi.org/project/wage-labor-record/):
  * jupyter-timetracker - GUI too complex/too close to DB editing tools. No support for clients
  * tim CLI only, no idle time detection but uses hledger as a backend!
  * salary-timetracker CLI only, tracking bound to git repos, fixed hourly rate but hey it uses CSV files!
  * ttrac CLI only, no idle time detection, no support for clients or tasks but uses JSON files!
  * tickertock only with a StreamDeck, wants to use cloud service as backend but uses a hardware interface!
  * mttt CLI only, no idle time detection but uses plain text files!
  * tt-cli CLI only, no idle time detection, no support for clients
  * timetracker CLI only, no idle time detection, no support for clients
  * 1k stars [hamster comes pretty close but seems outdated/abandoned and a little bit too complex](https://github.com/projecthamster/hamster)

[pages](http:/dvklopfenstein.github.io/timetracker)

Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved
