# Advanced usage


## Initialize a project
To begin to track time in a git-managed repo,
initialize your project for timetracking
while sitting at your git root directory:
```sh
# Where am I? Present Working Directory (pwd)
$ pwd
/home/bez/projects/meetinghouse

# Am I at the root of my git-managed repo? (yes)
$ git rev-parse --show-toplevel
/home/bez/projects/meetinghouse

# Initialize the meetinghouse project for timetracking
$ trk init
Ran `git add .timetracker/config .timetracker/.gitignore`
Initialized project directory: /home/bez/projects/meetinghouse/.timetracker
Added project to the global timetracker config: /home/bez/.timetrackerconfig:
  project: timetracker; config: /home/bez/projects/meetinghouse/.timetracker/config
```


### Initializing prepares the local project for time tracking
Initializing creates
a local project timetracker-csv
`config` file and a `.gitignore` file, which causes git to ignore temporary timetracker working files.
Both files are stored in the `.timetracker` directory at the project root.
```sh
$ pwd
/home/bez/projects/meetinghouse

$ find .timetracker/ -type f
.timetracker/.gitignore
.timetracker/config
```

See the [advanced usage](usage_advanced.md#initializing-runs-git-add)
more information about initialization and its options.


### Initializing adds the local project to the global config file
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
    ["meetinghouse", "/home/bez/projects/meetinghouse/.timetracker/config"],
    ["stonecutting",  "/home/bez/projects/stonecutting/.timetracker/config"],
]
```
The list of projects 
inside the global configuration file
is used for tasks such as:

  * Report total time spent on each project
  * Export a single CSV file containing all time entries for all projects.

### Initializing runs `git add`
If the project is git-managed, timetracker runs
`git add .timetracker/config .timetracker/.gitignore`,
which adds these timetracker files to your project's git repo:    
  * `.timetracker/config`
  * '.timetracker/.gitignore'
Use the `--no-git-add` option inhibit running `git add`.
```sh
$ trk init --no-git-add
Initialized project directory: /home/bez/projects/meetinghouse/.timetracker
Added project to the global timetracker config: /home/bez/.timetrackerconfig:
  project: timetracker; config: /home/bez/projects/meetinghouse/.timetracker/config
```

If you wish to "unadd" the timetracker files, do:
```sh
$ git reset .timetracker/.gitignore
$ git reset .timetracker/config
```

## Restarting the timer
### Restarting the timer with force
To restart the timer, even if it is currently running,
use the `--force` option with the `trk start` command.
```sh
trk 
Timer started on Tue 2025-04-01 05:08:24 AM and running H:M:S 3:39:16.348502 for 'trk' ID=bez
Run `trk stop -m "task description"` to stop tracking now and record this time unit

$ trk --trk-dir ./.trkr start --at 8am --force
Timer running; started Tue 2025-04-01 05:08:24 AM; running H:M:S 3:40:17.187956 for 'trk' ID=bez
Timetracker reset to: Tue 08:00 AM: 2025-04-01 08:00:00
```
### Starting the timer at the end of the last time unit

## Cancel the timer
To cancel the timer, use the `cancel` command.
```sh
$ trk init
Run `trk start` to start tracking

$ trk start
Timetracker started at: Tue 07:00 AM: 2025-04-01 07:00:00

$ trk cancel
Timer is canceled; was started Tue 2025-04-01 07:00:00 AM; running H:M:S 1:56:59.595338 for 'timetracker' ID=bez
```


## Specify a project timetracking directory
Specify a project timetracking directory
other than `.timetracker` using the `--trk-dir` option.

```sh
trk --trk-dir ./.trkr
Timer started on Tue 2025-04-01 05:08:24 AM and running H:M:S 3:39:16.348502 for 'trk' ID=bez
Run `trk stop -m "task description"` to stop tracking now and record this time unit
```

Copyright (C) 2025, DV Klopfenstein, PhD. All rights reserved
