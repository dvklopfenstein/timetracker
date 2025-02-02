Timetracker-csv
========


Installation
------------

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

## Quickstart
The `name` used by this time tracker is determined by the `USER` environmental variable by default.
### 1) Initialize a `.timetracker/` directory
```
$ trk init
Initialized empty timetracker directory: /PROJDIR/.timetracker for name(dvk)
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


Contents
--------

Copyright (C) 2025, DV Klopfenstein, PhD. All rights reserverd
