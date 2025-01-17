py:
	find tests timetracker bin -name \*.py

clean:
	rm -f test_timetracker.csv
	rm -f .timetracker_start
