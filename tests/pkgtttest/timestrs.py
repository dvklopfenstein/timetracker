#!/usr/bin/env python3
"""Free text containing datetimes"""

from datetime import datetime

NOW = datetime.today()

TIMESTRS = {
    # ========================================================
    # ========================================================
    '12am':{
        'exp_dct':{'hour': 0},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 0, 0, 0)
    },

    '12:01am':{
        'exp_dct':{'hour': 0, 'minute':1},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 0, 1, 0)
    },

    '12:15:30am':{
        'exp_dct':{'hour': 0, 'minute':15, 'second':30},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 0, 15, 30)
    },

    # --------------------------------------------------------
    '12pm':{
        'exp_dct':{'hour': 12},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 12, 0, 0)
    },

    '12:01pm':{
        'exp_dct':{'hour': 12, 'minute':1},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 12, 1, 0)
    },

    '12:45:15pm':{
        'exp_dct':{'hour': 12, 'minute':45, 'second':15},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 12, 45, 15)
    },

    # --------------------------------------------------------
    '12':{
        'exp_dct':{'hour': 12},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 12, 0, 0)
    },

    '12:01':{
        'exp_dct':{'hour': 12, 'minute':1},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 12, 1, 0)
    },

    '12:15:30':{
        'exp_dct':{'hour': 12, 'minute':15, 'second':30},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 12, 15, 30)
    },

    # --------------------------------------------------------
    '13':{
        'exp_dct':{'hour': 13},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 13, 0, 0)
    },

    '13:01':{
        'exp_dct':{'hour': 13, 'minute':1},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 13, 1, 0)
    },

    '13:45:15':{
        'exp_dct':{'hour': 13, 'minute':45, 'second':15},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 13, 45, 15)
    },

    # ========================================================
    # ========================================================
    '2025-01-02 12am':{
        'exp_dct':{'year': 2025, 'month': 1, 'day': 2, 'hour': 0},
        'dt': datetime(2025, 1, 2, 0, 0, 0)
    },

    '01-02 12:01am':{
        'exp_dct':{'month': 1, 'day': 2, 'hour': 0, 'minute':1},
        'dt': datetime(NOW.year, 1, 2, 0, 1, 0)
    },

    '1/2 12:01am':{
        'exp_dct':{'month': 1, 'day': 2, 'hour': 0, 'minute':1},
        'dt': datetime(NOW.year, 1, 2, 0, 1, 0)
    },

    '13/2 12:01am':{
        'exp_dct':None,
        'dt': None
    },

    '5pm':{
        'exp_dct':{'hour':17},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 17, 0, 0)
    },

    '13:23:00':{
        'exp_dct':{'hour':13, 'minute': 23, 'second': 0},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 13, 23, 0),
    },

    '2025':{
        'exp_dct': None,
        'dt': None,
    },

    '2025-06-10 08:57:12 AM':{
        'exp_dct':{'year': 2025, 'month': 6, 'day': 10,
                   'hour': 8, 'minute': 57, 'second': 12},
        'dt': datetime(2025, 6, 10, 8, 57, 12),
    },

    # ========================================================
    # ========================================================
    '06-10 08:57:12 AM':{
        'exp_dct':{'month': 6, 'day': 10,
                   'hour': 8, 'minute': 57, 'second': 12},
        'dt': datetime(2025, 6, 10, 8, 57, 12),
    },

    '6-10 08:57:12 AM':{
        'exp_dct':{'month': 6, 'day': 10,
                   'hour': 8, 'minute': 57, 'second': 12},
        'dt': datetime(2025, 6, 10, 8, 57, 12),
    },

    # timetracker-csv requires a value for an hour
    '2025-06-10':{'exp_dct': None, 'dt': None},

    '2025-06-10 8:57:12am':{
        'exp_dct':{'year': 2025, 'month': 6, 'day': 10,
                   'hour': 8, 'minute': 57, 'second': 12},
        'dt': datetime(2025, 6, 10, 8, 57, 12),
    },

    # ========================================================
    '13pm':{
        'exp_dct': None,
        'dt': None,
    },

    '5pm 3am':{
        'exp_dct':{'hour':3},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 3, 0, 0),
    },

    '5pm a 3am a ':{
        'exp_dct':{'hour':3},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 3, 0, 0),
    },
    '5pm xtra txt':{
        'exp_dct':{'hour':17},
        'dt': datetime(NOW.year, NOW.month, NOW.day, 17, 0, 0),
    },

    'ampm':{'exp_dct':None, 'dt':None},

}
