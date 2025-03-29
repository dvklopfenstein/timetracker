<!--
Copyright (C) 2025 DV Klopfenstein, PhD
License: https://www.gnu.org/licenses/agpl-3.0.en.html#license-text
-->

# Getting started

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

Copyright (C) 2025, DV Klopfenstein, PhD. All rights reserved
