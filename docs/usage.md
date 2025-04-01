<!--
Copyright 2025 DV Klopfenstein, PhD
License: https://www.gnu.org/licenses/agpl-3.0.en.html#license-text
-->

# Basic Usage #
**Timetracker-csv** tracks time one project repository at a time.

For a list of **timetracker-csv** commands, enter `trk --help`.

## Tracking time ##
A project repository is a directory that contains
project files and project sub-directories.

**Timetracker-csv** works seemlessly
with projects that are version-managed with `git`.
But it also works with any project.

To begin, initialize your project for timetracking:
```sh
# Initialize project for timetracking
$ trk init
Initialized timetracker directory: /home/bez/projects/meetinghouse/.timetracker
```

Initializing creates a local timetracker-csv config file for one project:
```sh
# The local project timetracker-csv config file
$ pwd
/home/bez/projects/meetinghouse

$ find .timetracker/ -type f
.timetracker/config
```
Initializing a timetracked project 
adds your project into a list containing
all of your timetracked projects
and is stored in a global configuration file.

The default global configuration file is `~/.timetrackerconfig`.
Each item in the list of timetracked projects contains both
the project name (e.g., `meetinghouse`) and 
the location of that project's local config file
(e.g., `/home/bez/projects/meetinghouse/.timetracker/config`).

```sh
# The global timetracker-csv config file contains a list of all projects
$ cat ~/.timetrackerconfig
projects = [
    ["timetracker",  "/home/bez/projects/timetracker/.timetracker/config"],
    ["meetinghouse", "/home/bez/projects/meetinghouse/.timetracker/config"],
]
```
The list of projects 
inside the global configuration file
is used for tasks such as:

  * Report total time spent on each project
  * Export a single csv file containing all time entries for all projects.


### Specifying Date and Time ###

The commands, `trk start` or `trk stop`,
use the current time for a start-time or a stop-time
unless otherwise specified by the researcher.

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

### Activities ###
There is one `Activity` column in each csv file.
For example, to add the activity, `docs`, to a time unit do:
```sh
$ trk stop -a docs -m "Document the ordered architecture for the meetinghouse"

# or the longer form (for shell scripts and makefiles)
$ trk stop --activity docs -m "Document meetinghouse architecture"
Timer stopped at Wed 2025-04-02 08:00:00 PM
Elapsed H:M:S 12:00:00 appended to timetracker_meetinghouse_bez.csv
```

### Tags ###
`trk` supports multiple tags per time entry.

For example, to add tags describing which metals are being crafted into various products, do:
```sh
$ trk stop -a art -t metal=gold product=lampstand -m "Crafted light holders for the meetinghouse"
Timer stopped at Thu 2025-04-03 09:00:00 PM
Elapsed H:M:S 13:00:00 appended to timetracker_meetinghouse_bez.csv
```
