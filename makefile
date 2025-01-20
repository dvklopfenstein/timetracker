py:
	find tests timetracker bin -name \*.py

pylint:
	git diff --name-only | perl -ne 'if (/(\S+\.py)/) {printf "echo $$1\npylint -r no %s\n", $$1}' | tee tmp_pylint
	chmod 755 tmp_pylint
	tmp_pylint

clean:
	rm -f test_timetracker.csv
	rm -f .timetracker_start
