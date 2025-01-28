# Timetracker-csv
Track time spent on multiple projects, one repo at a time.

A lightweight, repo-based, researcher name-based, command-line time tracker that stores data in csv spreadsheets.
![Work in progress](/doc/work_in_progress.png)
<p align="center"><img src="https://github.com/dvklopfenstein/timetracker/raw/main/docs/images/work_in_progress.png" alt="work in progress" width="500"/></p>


* [Advantages](#advantages)
* [Quickstart](#quickstart)
* [Installation](#installation)
* [Other time-trackers](#other-timetrackers)

## Advantages
* Freedom software (aka open-source)
* Own your data
* Human-readable ASCII data stored in csv files
* Modify your data if you forget to log time
* Quick to set up
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
### 1) Initialize a `.timetracker/` directory
```
$ trk init
Initialized empty timetracker directory: /DIR/.timetracker for name(dvk)
```
### 2) Start the timer
```
$ trk start
Timetracker started Wed 03:19 PM: 2025-01-22 15:19:46.479951 for name(dvk)
```
### 3) Stop the timer
```
$ trk stop -m 'Accomplished the planned task'
Elapsed H:M:S=0:01:36.981588 added to ./.timetracker/timetracker_dvk.csv
```
### 4) Reporting functions are coming...

## Installation
Install with pip:
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

Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved
