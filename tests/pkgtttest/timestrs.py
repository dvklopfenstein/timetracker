#!/usr/bin/env python3
"""Free text containing datetimes"""

from datetime import datetime

NOW = datetime.today()

TIMESTRS = {
    '12am':{
        'exp_dct':[{'hour': 12, 'AM/PM': 'AM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 0, 0, 0)
    },

    '12pm':{
        'exp_dct':[{'hour': 12, 'AM/PM': 'PM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 12, 0, 0)
    },

    '12:01am':{
        'exp_dct':[{'hour': 12, 'minute':1, 'AM/PM': 'AM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 0, 1, 0)
    },

    '12:15:30am':{
        'exp_dct':[{'hour': 12, 'minute':15, 'second':30, 'AM/PM': 'AM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 0, 15, 30)
    },

    '12:01pm':{
        'exp_dct':[{'hour': 12, 'AM/PM': 'PM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 12, 1, 0)
    },

    '12:45:15pm':{
        'exp_dct':[{'hour': 12, 'AM/PM': 'PM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 12, 45, 15)
    },

    '5pm':{
        'exp_dct':[{'hour':5, 'AM/PM':'PM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 17, 0, 0)
    },

    '13:23:00':{
        'exp_dct':[{'hour':13, 'minute': 23, 'second': 0}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 13, 23, 0),
    },

    '2025':{
        'exp_dct':[{'year': 2025}],
        'dt': None,
    },

    '2025-06-10 08:57:12 AM':{
        'exp_dct':[{'year': 2025, 'month': 6, 'day': 10},
                   {'hour': 8, 'minute': 57, 'second': 12, 'AM/PM':'AM'}],
        'dt': datetime(2025, 6, 10, 8, 57, 12),
    },

    #'06-10 08:57:12 AM':{
    #    'exp_dct':[{'year': 2025, 'month': 6, 'day': 10},
    #               {'hour': 8, 'minute': 57, 'second': 12, 'AM/PM':'AM'}],
    #    'dt': datetime(2025, 6, 10, 8, 57, 12),
    #},

    #'6-10 08:57:12 AM':{
    #    'exp_dct':[{'year': 2025, 'month': 6, 'day': 10},
    #               {'hour': 8, 'minute': 57, 'second': 12, 'AM/PM':'AM'}],
    #    'dt': datetime(2025, 6, 10, 8, 57, 12),
    #},

    #'2025-06-10':{
    #    'exp_dct':[{'year': 2025, 'month': 6, 'day': 10},
    #               {'hour': NOW.hour, 'minute': NOW.minute, 'second': NOW.second}],
    #    'dt': datetime(2025, 6, 10, NOW.hour, NOW.minute, NOW.second),
    #},

    '2025-06-10 8:57:12am':{
        'exp_dct':[{'year': 2025, 'month': 6, 'day': 10},
                   {'hour': 8, 'minute': 57, 'second': 12, 'AM/PM':'AM'}],
        'dt': datetime(2025, 6, 10, 8, 57, 12),
    },

    '13pm':{
        'exp_dct':[{'hour': 13, 'AM/PM': 'PM'}],
        'dt': None,
    },

    '5pm 3am':{
        'exp_dct':[{'hour':5, 'AM/PM':'PM'},
                   {'hour':3, 'AM/PM':'AM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 3, 0, 0),
    },

    '5pm a 3am a ':{
        'exp_dct':[{'hour':5, 'AM/PM':'PM'},
                   {'hour':3, 'AM/PM':'AM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 3, 0, 0),
    },
    '5pm xtra txt':{
        'exp_dct':[{'hour':5, 'AM/PM':'PM'}],
        'dt': datetime(NOW.year, NOW.month, NOW.day, 17, 0, 0),
    },

    'ampm':{'exp_dct':[], 'dt':None},

}
