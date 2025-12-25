MAKEFLAGS := --no-print-directory

PYTHON := python3
CSV := ~/timetrackers/timetracker_trk_dvklo.csv

dox:
	find doc/mkdocs

install:
	pip install .

py:
	find tests timetracker -name \*.py

DAYS=-1
pn:
	find tests timetracker -mtime $(DAYS) -name \*.py


DIRTRK = ./.trkr
PROJ = trk
trk:
	trk --trk-dir $(DIRTRK)

# -----------------------------------------------------------------------------
init:
	rm -rf $(DIRTRK)
	trk --trk-dir $(DIRTRK) init --project $(PROJ) --csvdir ~/timetrackers
	find $(DIRTRK)

start:
	trk --trk-dir $(DIRTRK) start
	find $(DIRTRK)
	@grep -Hw --color filename $(DIRTRK)/config
	@ls -lrt ../timetrackers/timetracker_trk_$(USER).csv
	find $(DIRTRK)

cancel:
	trk --trk-dir $(DIRTRK) cancel
	find $(DIRTRK)
	@grep -Hw --color filename $(DIRTRK)/config
	@ls -lrt ~/timetrackers/timetracker_trk_$(USER).csv
	find $(DIRTRK)

# Test that researcher passed a stop message using M="This is my stop message"
# https://stackoverflow.com/questions/51535230/makefile-test-if-variable-is-not-empty
stop:
	find $(DIRTRK)
	@echo "~/timetrackers/timetracker_trk_$(USER).csv"
	@if [ -n "$$M" ]; then \
	  make _stop; \
	else  \
	  echo '$@ MESSAGE FATAL: USAGE: make stop M="Describe activities in timeblock"'; \
		false ; \
	fi

_stop:
	#trk --trk-dir $(DIRTRK) stop -m "\"$(M)\""
	trk --trk-dir $(DIRTRK) stop -m "$(M)"
	find $(DIRTRK)
	grep filename $(DIRTRK)/config
	#find ~/timetrackers/ -type f -name \*.csv

report:
	trk --trk-dir $(DIRTRK) report

projects:
	trk --trk-dir $(DIRTRK) projects

csv:
	trk --trk-dir $(DIRTRK) csv

hours:
	trk --trk-dir $(DIRTRK) hours

	
files:
	@grep -nH --color filename $(DIRTRK)/config
	@echo "~/timetrackers/timetracker_trk_$(USER).csv"
	find $(DIRTRK)
	find .timetracker

defs:
	find . -name \*.py | xargs grep -nw --color def | grep -v self | grep -w --color def


# -----------------------------------------------------------------------------
# 1) Increase the version number:
vim_ver:
	vim -p timetracker/__init__.py pyproject.toml CHANGELOG.md

# -----------------------------------------------------------------------------
./doc/mkdocs/source/contributing.md: CONTRIBUTING.md
	cp $< $@

clean_build:
	rm -rf build/
	rm -rf timetracker_csv.egg-info/
	rm -rf dist/

clean_pycache:
	find . -type d -name __pycache__ | xargs rm -rf

cltt:
	rm -rf .timetracker/

clean:
	make ./doc/mkdocs/source/contributing.md
	make clean_build
	make clean_pycache
	rm -f test_timetracker.csv
	rm -f .timetracker_start
	rm -f timetracker_*.csv
	rm -f updated.csv
	rm -f .timetracker_starttime
	rm -rf tmp; mkdir tmp;
	rm -f *.docx
	rm -f .timetracker_starttime
	rm -f *.cfg
	rm -f timetrials_datatime.csv

clobber:
	make clean
	rm -rf .timetracker/ .tt/
	rm -f timetracker_timetracker_dvklo.csv
	rm -rf site
