## Viewing and Searching Entries ##

-```text
-This is an example of text.
 ```

-!!! note
-    This is an example of a note.


`trk` can display entries in a variety of ways.

To view all entries, enter:
```sh
trk -to today
```

`trk` provides several filtering commands, prefaced by a single dash (`-`), that
allow you to find a more specific range of entries. For example,

```sh
trk -n 10
```

lists the ten most recent entries. `trk -10` is even more concise and works the
same way. If you want to see all of the entries you wrote from the beginning of
last year until the end of this past March, you would enter

```sh
trk -from "last year" -to march
```

Filter criteria that use more than one word require surrounding quotes (`""`).

To see entries on a particular date, use `-on`:
```sh
trk -on yesterday
```

### Text Search ###

The `-contains` command displays all entries containing the text you enter after it.
This may be helpful when you're searching for entries and you can't remember if you
tagged any words when you wrote them.

You may realize that you use a word a lot and want to turn it into a tag in all
of your previous entries.

```sh
trk -contains "dogs" --edit
```

opens your external editor so that you can add a tag symbol (`@` by default) to
all instances of the word "dogs."

### Filtering by Tag ###

You can filter your time entries by tag. For example,

```sh
trk @pinkie @WorldDomination
```

displays all entries in which either `@pinkie` or `@WorldDomination`
occurred. Tag filters can be combined with other filters:

```sh
trk -n 5 @pinkie -and @WorldDomination
```

displays the last five entries containing _both_ `@pinkie` _and_
`@worldDomination`. You can change which symbols you'd like to use for tagging
in the [configuration file](./reference-config-file.md#tagsymbols).

!!! note
    Entering `trk @pinkie @WorldDomination` will display entries in which both
    tags are present because, although no command line arguments are given, all
    of the input strings look like tags. `trk` will assume you want to filter
    by tag, rather than create a new entry that consists only of tags.

To view a list of all of your tags in the current timetracker-csv project, enter:

```sh
trk tag
```

### Viewing Starred Entries ###

To display only your favorite (starred) entries, enter

```sh
trk -starred
```

## Editing Entries ##

You can edit entries after writing them. This is particularly useful when your
time file is encrypted. To use this feature, you need to have an external
editor configured in your [configuration file](./reference-config-file.md#editor). You
can also edit only the entries that match specific search criteria. For example,

```sh
trk -to 1950 @texas -and @history --edit
```

opens your external editor displaying all entries tagged with `@texas` and
`@history` that were written before 1950. After making changes, save and close
the file, and only those entries will be modified (and encrypted, if
applicable).

If you are using multiple times, it's easy to edit specific entries from
specific times. Simply prefix the filter string with the name of the time.
For example,

```sh
trk work -n 1 --edit
```

opens the most recent entry in the 'work' time in your external editor.

## Deleting Entries ##

The `--delete` command opens an interactive interface for deleting entries. The
date and title of each entry in the time are presented one at a time, and you
can choose whether to keep or delete each entry.

If no filters are specified, `trk` will ask you to keep or delete each entry in
the entire time, one by one. If there are a lot of entries in the time, it
may be more efficient to filter entries before passing the `--delete` command.

Here's an example. Say you have a time into which you've imported the last 12
years of blog posts. You use the `@book` tag a lot, and for some reason you want
to delete some, but not all, of the entries in which you used that tag, but only
the ones you wrote at some point in 2004 or earlier. You're not sure which
entries you want to keep, and you want to look through them before deciding.
This is what you might enter:

```sh
trk -to 2004 @book --delete
```

`trk` will show you only the relevant entries, and you can choose the ones you
want to delete.

You may want to delete _all_ of the entries containing `@book` that you wrote in
2004 or earlier. If there are dozens or hundreds, the easiest way would be to
use an external editor. Open an editor with the entries you want to delete...

```sh
trk -to 2004 @book --edit
```

...select everything, delete it, save and close, and all of those entries are
removed from the time.

## Listing Journals ##

To list all of your times:

```sh
trk --list
```

The times displayed correspond to those specified in the `trk`
[configuration file](./reference-config-file.md#times).
