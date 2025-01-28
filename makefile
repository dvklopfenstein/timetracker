MAKEFLAGS := --no-print-directory
PYTHON := python3

install:
	pip install .

py:
	find tests timetracker bin -name \*.py
	find .timetracker -type f

.PHONY: c
c:
	cat .timetracker/start_dvklo.txt

pylint:
	git diff --name-only | perl -ne 'if (/(\S+\.py)/) {printf "echo $$1\npylint -r no %s\n", $$1}' | tee tmp_pylint
	chmod 755 tmp_pylint
	tmp_pylint

init:
	trk init --csvdir ~/timetrackers/projs/
	make show

stop:
	trk stop -m test
	find .timetracker
	grep filename .timetracker/config
	find ~/timetrackers/projs
	
show:
	find ~/timetrackers/projs
	find .timetracker/
	cat .timetracker/config

.pylintrc:
	pylint --generate-rcfile > .pylintrc

# -----------------------------------------------------------------------------
# 1) Increase the version number:
vim_ver:
	vim -p timetracker/__init__.py setup.py CHANGELOG.md

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


# -----------------------------------------------------------------------------
upgrade:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install --upgrade setuptools
	$(PYTHON) -m pip install --upgrade wheel
	$(PYTHON) -m pip install --upgrade twine

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

clobber:
	make clean
	rm -rf .timetracker/
