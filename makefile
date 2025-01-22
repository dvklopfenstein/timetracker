MAKEFLAGS := --no-print-directory

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

clean_build:
	rm -rf build/
	rm -rf timetracker.egg-info/

clean:
	make clean_build
	rm -f test_timetracker.csv
	rm -f .timetracker_start

clobber:
	rm -rf .timetracker/
