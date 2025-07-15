# Invoicing

----------------------------------------------------------------------------------
## Quickstart invoicing
### Mark timeslots as `Billable`
To mark an item as billable, use the `--billable` or `-b` option in the `stop` command:
```sh
$ trk start
Timetracker started at: Wed 08:00 AM: 2025-06-04 08:00:00

$ trk stop --billable --message "Defined meetinghouse project goals, budget, and timeline"
or
$ trk stop -b -m "Defined meetinghouse project goals, budget, and timeline"
Timetracker stopped at: Wed 2025-06-04 05:00:00 PM: 2025-06-04 17:00:00
Elapsed H:M:S 9:00:00 appended to timetracker_meetinghouse_bez.csv
```

### Get an invoice of billable items
All items `tag`ed with `Billable` will be included in the invoice:
```sh
```

----------------------------------------------------------------------------------
## Advanced invoicing
To create an invoice for a project while the current working directory
is not in the time-tracked repo, use the `--trk-dir` option:
```sh
$ trk --trk-dir ../antimicrobial_stewardship/.timetracker/ invoice
  WROTE: report.docx
```

