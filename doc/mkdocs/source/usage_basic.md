<!--
Copyright 2025 DV Klopfenstein, PhD
License: https://www.gnu.org/licenses/agpl-3.0.en.html#license-text
-->

# Basic Usage #
**Timetracker-csv** tracks time one project repository (repo) at a time.

For a list of **timetracker-csv** commands, enter `trk --help`.

## Projects ##
**Timetracker-csv** works seemlessly
with projects that are version-managed with `git`.
But it also works with any project.

If you use `git`, then each git-managed project repository (repo)
will also be a trk-managed project.
This means that time will be saved in separate
CSV files for separate repos.

Multiple CSV files can be combined
into a single CSV file
using the `trk export` command.


## CSV files
Comma-separated value
([CSV](https://www.datarisy.com/blog/understanding-csv-files-use-cases-benefits-and-limitations))
files store tabular data in plain text.
CSV files are readable by both humans and computers.

### CSV rows and columns
Each time unit is stored in a single row.
Each row contains five columns:

Name       | Required | Example
-----------|----------|------------------
Start time | required | 9am Monday, March 31, 2025
Duration   | required | 2 hours
Activity   | optional | "documenting" or "coding"
Description| required | Made decorative almond tree blossoms out of gold
Tags       | optional | grant=ABC, grant=XYZ, art, metalwork

* **Start time**: Determined automatically upon running `trk start`
* **Duration**: Calculated automatically upon running
  `trk stop -m msg`
* **Activity**: There can be one activity per time unit.
* **Description**: Just as a `git commit` message is mandatory,
  so is a `trk stop` message, which describes the work that was done in the time unit.
* **Tags**: There can be any number of tags per time unit.
  Tags can be of the form `key=value` or simply `value`.

### CSV files for a single project
There is one CSV file written per user per project.
Therefore, a single project repository will have more than
one CSV file if there is more than one
person working on the project.
Having one project CSV file per person (username) prevents
conflicts when using `git` to commit timetracking csv files.

People commonly use
[pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/01_table_oriented.html#min-tut-01-tableoriented)
to analyze and plot data contained in CSV files.

Multiple CSV files can be combined
into a single CSV file
using the `trk export` command.


## Initialize a project
To begin to track time in a git-managed repo,
initialize your project for timetracking
while sitting at your git root directory:
```sh
# Where am I? Present Working Directory (pwd)
$ pwd
/home/bez/projects/meetinghouse

# Initialize the meetinghouse project for timetracking
$ trk init
Ran `git add .timetracker/config .timetracker/.gitignore`
Initialized project directory: /home/bez/projects/meetinghouse/.timetracker
Added project to the global timetracker config: /home/bez/.timetrackerconfig:
  project: timetracker; config: /home/bez/projects/meetinghouse/.timetracker/config
```


## Start and stop the timer
The commands, `trk start` or `trk stop`,
use the current time for a start-time or a stop-time
unless otherwise specified by the researcher.
```sh
$ trk start
Timetracker started at: Mon 09:00 AM: 2025-03-31 09:00:00
```

Just as `git` requires a message when running `git commit`,
`trk` also requires a message when stopping the timer:
```sh
$ trk stop -m "Received skills necessary for the job"
Timer stopped at Mon 2025-03-31 11:30:00 AM
Elapsed H:M:S 2:30:00 appended to timetracker_meetinghouse_bez.csv
```

Researchers may find it convenient to reuse a message
for both stopping the timer and commiting files
use the `!$` [shell variable](https://stackoverflow.com/a/5163158):
```sh
$ trk stop -m "Received skills necessary for the job"
Timer stopped at Mon 2025-03-31 11:30:00 AM
Elapsed H:M:S 2:30:00 appended to timetracker_meetinghouse_bez.csv

$ git commit -a -m !$
git commit -a -m 'Received skills necessary for the job'
[main 8d2d5e1] Received skills necessary for the job
8 files changed, 33 insertions(+)
# or use the long version of the `git commit` options:
#   $ git commit --all --message=!$
```

## Specify a date and time
Explicitly specify a start and/or stop time, with the `--at` option
(e.g. `trk start --at 9am` and `trk stop --at 5:3pm`):
```sh
$ trk start --at 9am
Timetracker started at: Mon 09:00 AM: 2025-03-31 09:00:00

$ trk stop --at 5:30pm -m "Discuss the appointment of the meetinghouse architect"
Timer stopped at Mon 2025-03-31 05:30:00 PM
Elapsed H:M:S 8:30:00 appended to timetracker_meetinghouse_bez.csv
```

To preview a date and time determined from a given time string,
use **timetracker-csv**'s `timestr` command:
```sh
$ date
Mon, Mar 31, 2025  2:50:06 PM

$ timestr "9am monday"
2025-03-24 09:00:00        <- "9am monday"

$ timestr "noon"
2025-03-31 12:00:00        <- "noon"

$ timestr "23 march 2025 8:30am"
2025-03-23 08:30:00        <- "23 march 2025 8:30am"

$ timestr "3/25 at 5:30pm"
2025-03-25 17:30:00        <- "3/25 at 5:30pm"

$ timestr "2025-03-01T15:55-04:00"
2025-03-01 15:55:00-04:00  <- "2025-03-01T15:55-04:00"
```

### Track your time
Use the `start` and `stop` commands to record time:
```sh
$ trk start --at 9am
Timetracker started at: Mon 09:00 AM: 2025-03-31 09:00:00

$ trk stop --at 11:30am -m "Received skills necessary for the job"
Timer stopped at Mon 2025-03-31 11:30:00 AM
Elapsed H:M:S 2:30:00 appended to timetracker_meetinghouse_bez.csv

$ trk start --at 12:30pm
Timetracker started at: Mon 12:30 PM: 2025-03-31 12:30:00

$ trk stop --at 3pm -m "Trained apprentices in decorative art"
Timer stopped at Mon 2025-03-31 03:00:00 PM
Elapsed H:M:S 2:30:00 appended to timetracker_meetinghouse_bez.csv

$ trk start --at 3pm
Timetracker started at: Mon 03:00 PM: 2025-03-31 15:00:00

$ trk stop --at 3:30pm -m "Began crafting a chest from Acacia wood to store crucial docs"
Timer stopped at Mon 2025-03-31 03:30:00 PM
Elapsed H:M:S 0:30:00 appended to timetracker_meetinghouse_bez.csv

$ trk start --at 3:30pm
Timetracker started at: Mon 03:30 PM: 2025-03-31 15:30:00

$ trk stop  --at 5:30pm -m "Covered chest in gold"
Timer stopped at Mon 2025-03-31 05:30:00 PM
Elapsed H:M:S 2:00:00 appended to timetracker_meetinghouse_bez.csv

$ trk hours
7:30:00 H:M:S or 7.500 hours

$ trk report
Day  Date        Span     Total  Description
---  ----------  -----    -----  -----------------------------------
Mon  2025-03-31  02:30    02:30  Received skills necessary for the job
Mon  2025-03-31  02:30    05:00  Trained apprentices in decorative art
Mon  2025-03-31  00:30    05:30  Began crafting a chest from Acacia wood to store crucial docs
Mon  2025-03-31  02:00    07:30  Covered chest in gold
```

## Show running timers
Show all timers that are currently running in either
the default concise format or the verbose format.

### Concise format
Bez is the researcher whose username is `bez`.
Bez is currently working on three projects:
`architecture`, `stonecutting`, and `cabinetry`.

The command, `trk running` will show
the day and time that the timer was started (`Tue 2025-07-15 11:56:17 AM`) and
the elapsed time in hours, minutes, and seconds (`H:M:S 1:04:45`).

```sh
$ trk running
Began Tue 2025-07-15 11:56:17 AM -> H:M:S 1:04:45 by bez for architecture
Began Tue 2025-07-15 11:35:40 AM -> H:M:S 1:25:22 by bez for stonecutting
Began Tue 2025-07-15 12:00:00 PM -> H:M:S 1:01:03 by bez for cabinetry
3 of 37 projects have running timers; listed in: /home/bez/.timetrackerconfig
```

### Verbose format
Using `--verbose` will show the directory for each project that has a running timer.
In this example, each project directory is in the `/home/bez/projs/` directory.
```sh
$ architecture running -v
Began Tue 2025-07-15 11:56:17 AM -> H:M:S 1:06:35 by bez for architecture
    /home/bez/projs/architecture

Began Tue 2025-07-15 11:35:40 AM -> H:M:S 1:27:12 by bez for stonecutting
    /home/bez/projs/stonecutting

Began Tue 2025-07-15 12:00:00 PM -> H:M:S 1:02:53 by bez for cabinetry
    /home/bez/projs/cabinetry

3 of 37 projects have running timers; listed in: /home/bez/.timetrackerconfig
```


## Activities
There is one `Activity` column in each CSV file.
For example, to add the activity, `docs`, to a time unit do:
```sh
$ trk stop -a docs -m "Document the ordered architecture for the meetinghouse"

# or the longer form (for shell scripts and makefiles)
$ trk stop --activity docs -m "Document meetinghouse architecture"
Timer stopped at Wed 2025-04-02 08:00:00 PM
Elapsed H:M:S 12:00:00 appended to timetracker_meetinghouse_bez.csv
```

## Tags
`trk` supports multiple tags per time entry.
Tags can be of the format, `key=value`, or simply `value`.

For example, to add tags describing which metals are being crafted into various products, do:
```sh
$ trk stop -a art -t metal=gold product=lampstand -m "Crafted light holders for the meetinghouse"
Timer stopped at Thu 2025-04-03 09:00:00 PM
Elapsed H:M:S 13:00:00 appended to timetracker_meetinghouse_bez.csv
```
