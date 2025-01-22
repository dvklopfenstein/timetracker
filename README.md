# Timetracker
A lightweight, repo-based, command-line time tracker that stores data in csv files.

Helps to track time spent on multiple projects, one repo at a time.

# Advantages
* Freedom software (aka open-source)
* Own your data
* Human-readable ASCII data
* Modify your data if you forget to log time
* Quick to set up
* Quickly see the current task being recorded
* Quickly see elapsed time spent on the current task
* No clicking and clicking and clicking on a GUI
* Does not require the internet or any cloud-based services

# Quickstart
## 1) Initialize a `.timetracker/` directory
```
$ trkr init
```

# Installation
```
$ git clone git@github.com:dvklopfenstein/timetracker.git
$ cd timetracker
$ pip install .
```

# Other timetrackers
* 13k stars [ActivityWatch](https://github.com/ActivityWatch/activitywatch)
* 5 start [Jupyter timetracker](https://github.com/PrateekKumarPython/jupyter-timetracker) uses aTimeLogger csv format
* https://atimelogger.pro/ csv files
* [List of timetrackers in PyPi](https://pypi.org/search/?q=timetracker)
* [web-based time tracking application](https://github.com/anuko/timetracker)
* [Wage Labor record](https://pypi.org/project/wage-labor-record/)
  * jupyter-timetracker - GUI too complex/too close to DB editing tools. No support for clients
  * tim CLI only, no idle time detection but uses hledger as a backend!
  * salary-timetracker CLI only, tracking bound to git repos, fixed hourly rate but hey it uses CSV files!
  * ttrac CLI only, no idle time detection, no support for clients or tasks but uses JSON files!
  * tickertock only with a StreamDeck, wants to use cloud service as backend but uses a hardware interface!
  * mttt CLI only, no idle time detection but uses plain text files!
  * tt-cli CLI only, no idle time detection, no support for clients
  * timetracker CLI only, no idle time detection, no support for clients
  * 1k stars [hamster comes pretty close but seems outdated/abandoned and a little bit too complex](https://github.com/projecthamster/hamster)

Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved
