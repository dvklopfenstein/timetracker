<!--
Copyright (C) 2025 DV Klopfenstein, PhD
License: https://www.gnu.org/licenses/agpl-3.0.en.html#license-text
-->

# Getting started

## Installation
Install with [timetracker-csv](https://pypi.org/project/timetracker-csv/) pip:
```sh
$ pip install --upgrade timetracker-csv
```
Or install from source:
```sh
$ git clone git@github.com:dvklopfenstein/timetracker.git
$ cd timetracker
$ pip install .
```

## Quickstart
The `name` used by this time tracker is determined by the `USER` environmental variable by default.
### [1) Initialize a timetracker project](usage_basic.md#initialize-a-project)
```sh
$ cd /home/bez/projects/meetinghouse

$ trk init
Ran `git add .timetracker/config .timetracker/.gitignore`
Initialized project directory: /home/bez/projects/meetinghouse/.timetracker
Added project to the global timetracker config: /home/bez/.timetrackerconfig:
  project: meetinghouse; config: /home/bez/projects/meetinghouse/.timetracker/config
```
### 2) Start the timer
```sh
$ trk start
Timetracker started now: Mon 09:00 AM: 2025-03-24 09:00:00
```
### 3) Stop the timer
```sh
$ trk stop -m 'Received architectural plans'
Timer stopped at Mon 2025-03-24 12:00:00 PM
Elapsed H:M:S 0:03:00 appended to timetracker_meetinghouse_bez.csv
```
### 4) Report my time units for this project
```sh
$ trk report
Day  Date        Span     Total  Description
Sun  2025-03-24  03:00    03:00  Received architectural plans
```
You can also get the total hours that you spent on a project:
```sh
$ trk hours
0:03:00 H:M:S or 3.000 hours
```

Copyright (C) 2025, DV Klopfenstein, PhD. All rights reserved
