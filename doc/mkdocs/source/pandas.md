# Timetracker csv files and pandas

## Quickstart
```
import pandas as pd

df = pd.read_csv("timetracker_meetinghouse_bez.csv")
df['start_datetime'] = pd.to_datetime(df['start_datetime'], format='ISO8601')
df['duration'] = pd.to_timedelta(df['duration'])
```


