# Advanced usage
Under construction...

## Restarting the timer
To restart the timer, use the `--force` option with the `trk start` command.
```
trk 
Timer started on Tue 2025-04-01 05:08:24 AM and running H:M:S 3:39:16.348502 for 'trk' ID=bez
Run `trk stop -m "task description"` to stop tracking now and record this time unit

$ trk --trk-dir ./.trkr start --at 8am --force
Timer running; started Tue 2025-04-01 05:08:24 AM; running H:M:S 3:40:17.187956 for 'trk' ID=bez
Timetracker reset to: Tue 08:00 AM: 2025-04-01 08:00:00
```

## Cancel the timer
To cancel the timer, use the `cancel` command.
```
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

```
trk --trk-dir ./.trkr
Timer started on Tue 2025-04-01 05:08:24 AM and running H:M:S 3:39:16.348502 for 'trk' ID=bez
Run `trk stop -m "task description"` to stop tracking now and record this time unit
```

Copyright (C) 2025, DV Klopfenstein, PhD. All rights reserved
