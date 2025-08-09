<!--
Copyright (C) DV Klopfenstein, PhD
License: https://www.gnu.org/licenses/agpl-3.0.en.html#license-text
https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup
-->
<p align="center" style="display:inline">
<h1 align="center">Timetracker-csv</h1>
<h3 align="center">Pandas-friendly time tracking from the CLI, repo by repo</h3>
<h3 align="center">
<a href="https://pypi.org/project/timetracker-csv"><img src="https://img.shields.io/pypi/v/timetracker-csv" alt="PyPI - Version"></a> |
<a href="https://doi.org/10.5281/zenodo.14803226"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.14803226.svg" alt="DOI"></a> |
<a href="https://www.gnu.org/licenses/agpl-3.0.en.html"><img src="https://img.shields.io/github/license/dvklopfenstein/timetracker" alt="License"></a>
</h3>
<pre align="center" style="font-family: monospace; font-size: larger; border: 1px solid #ccc; padding: 10px; display: inline-block;">
┌────────────────────────────┐
│ 🕒 Timetracker CLI Tool    │
│ Track time → CSV → pandas  │
└────────────────────────────┘
</pre>
</p>

Track time spent on multiple projects,
one repo at a time from the [CLI](https://blog.iron.io/pros-and-cons-of-a-command-line-interface)    

Time is saved in
[pandas](https://pandas.pydata.org/pandas-docs/stable/index.html)-friendly plaintext
[CSV](https://www.datarisy.com/blog/understanding-csv-files-use-cases-benefits-and-limitations) files

<p align="center"><img src="https://github.com/dvklopfenstein/timetracker/raw/main/doc/mkdocs/source/images/stopwatch.png" alt="timetracker" width="750"/></p>

## Description
Timetracker is a
lightweight, privacy-respecting CLI tool
that logs your work sessions into
clean, pandas-friendly CSV files.
Whether you're juggling multiple projects or
just want a no-fuss way to monitor your productivity,
Timetracker keeps your data local, editable, and analysis-ready.
* No cloud. No surveillance.
* Human-readable logs perfect for Python and pandas workflows.
* Quick to set up, easy to use, and fully open source.
* Supports free-form messages, optional activity types, and tag metadata

## Quickstart
The username of the researcher running this timer is "bez."
The project repository (repo) name is "meetinghouse."
```sh
#----------------------------------------------------
# 1) Initialize a timetracker project
$ cd /home/bez/projs/meetinghouse

$ trk init --csvdir doc/
or
$ trk init --d doc/
Initialized timetracker directory: /home/bez/projs/meetinghouse/.timetracker

#----------------------------------------------------
# 2) Start the timer
$ trk start
Timetracker started now: Mon 09:00 AM: 2025-03-24 09:00:00
```

Initializing with the option `--csvdir doc/` (`-d doc/`)
will cause time units to be written to
a csv file stored in the `doc/` directory,
rather than in the default repo root directory.
```sh
#----------------------------------------------------
# 3) Stop the timer
$ trk stop -m 'Received instructions'
Timer stopped at Mon 2025-03-24 12:00:00 PM
Elapsed H:M:S 0:03:00 appended to doc/timetracker_meetinghouse_bez.csv

#----------------------------------------------------
# 4a) Report my time units for this project
$ trk report
Day  Date        Span     Total  Description
Sun  2025-03-24  03:00    03:00  Received instructions

#- - - - - - - - - - - - - - - - - - - - - - - - - - 
# 4b) Get my total hours spent on the project:
$ trk hours
0:03:00 H:M:S or 3.000 hours
```

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

Copyright (C) 2025, DV Klopfenstein, PhD. All rights reserved
