MAKEFLAGS := --no-print-directory
PYTHON := python3
CSV := /home/dvklo/timetrackers/timetracker_trk_dvklo.csv

install:
	pip install .

py:
	find tests timetracker bin -name \*.py

DAYS=-1
pn:
	find tests timetracker bin -mtime $(DAYS) -name \*.py


DIRTRK = ./.trkr
PROJ = trk
trk:
	trk -f $(GLOBCFG) --trk-dir $(DIRTRK)

# -----------------------------------------------------------------------------
init:
	rm -rf $(DIRTRK)
	trk -f $(GLOBCFG) --trk-dir $(DIRTRK) init --project $(PROJ) --csvdir ~/timetrackers
	find $(DIRTRK)

start:
	trk -f $(GLOBCFG) --trk-dir $(DIRTRK) start
	find $(DIRTRK)
	@grep -Hw --color filename $(DIRTRK)/config
	@ls -lrt ~/timetrackers/timetracker_trk_$(USER).csv
	find $(DIRTRK)

cancel:
	trk -f $(GLOBCFG) --trk-dir $(DIRTRK) cancel
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
	#trk -f $(GLOBCFG) --trk-dir $(DIRTRK) stop -m "\"$(M)\""
	trk -f $(GLOBCFG) --trk-dir $(DIRTRK) stop -m "$(M)"
	find $(DIRTRK)
	grep filename $(DIRTRK)/config
	#find ~/timetrackers/ -type f -name \*.csv

report:
	trk -f $(GLOBCFG) --trk-dir $(DIRTRK) report

projects:
	trk -f $(GLOBCFG) --trk-dir $(DIRTRK) projects

csv:
	trk -f $(GLOBCFG) --trk-dir $(DIRTRK) csv

time:
	trk -f $(GLOBCFG) --trk-dir $(DIRTRK) time

docx:
	trk -f $(GLOBCFG) --trk-dir $(DIRTRK) time -i $(CSV)
	trk -f $(GLOBCFG) --trk-dir $(DIRTRK) invoice -i $(CSV) -o timetracker.docx

	
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
	vim -p timetracker/__init__.py setup.py pyproject.toml CHANGELOG.md

# 2) Create wheel - Check PyPi packages are up-to-date: make upgrade
# https://packaging.python.org/guides/distributing-packages-using-setuptools/#packaging-your-project
# universal wheels are pure Python
#   Needs wheel package to run bdist_wheel: pip3 install wheel
.PHONY: build
build:
	# python3 -m pip install -U pip
	# python3 -m pip install --user --upgrade setuptools wheel
	make clean_build
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel --universal
	ls -lh dist
	twine check dist/*

# 3) Upload wheel to https://pypi.org
# https://pypi.org/manage/account/token/
# python3 -m pip install --upgrade timetracker
upload:
	#twine upload dist/* --verbose
	twine upload dist/* --repository timetracker-csv --verbose

# https://stackoverflow.com/questions/5667884/how-to-squash-commits-in-git-after-they-have-been-pushed
# https://stackoverflow.com/questions/35979642/what-is-git-tag-how-to-create-tags-how-to-checkout-git-remote-tags
upgrade:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install --upgrade setuptools
	$(PYTHON) -m pip install --upgrade wheel
	$(PYTHON) -m pip install --upgrade twine

# -----------------------------------------------------------------------------
clean_build:
	rm -rf build/
	rm -rf timetracker_csv.egg-info/
	rm -rf dist/

clean_pycache:
	find . -type d -name __pycache__ | xargs rm -rf

cltt:
	rm -rf .timetracker/

clean:
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

clobber:
	make clean
	rm -rf .timetracker/ .tt/
	rm -f timetracker_timetracker_dvklo.csv
