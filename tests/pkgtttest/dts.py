r"""Get start dates for tests from:
   In the Year 2525 (Exordium & Terminus)
   by Zager & Evans (1969)

ex·or·di·um (noun) plural exordiums \-ēəmz\or exor·dia\-ēə\
    : beginning, introduction  especially
    : the introductory part of a discourse or composition

ter·mi·nus (noun) plural termi·ni \-nī, ˌnē\ or terminuses
    : final goal of a journey or an endeavor
    : finishing point
    : end  also
    : starting point

“Exordium.” Merriam-Webster's Unabridged Dictionary, Merriam-Webster,
https://unabridged.merriam-webster.com/unabridged/exordium. Accessed 21 Feb. 2025.

“Terminus.” Merriam-Webster's Unabridged Dictionary, Merriam-Webster,
https://unabridged.merriam-webster.com/unabridged/terminus. Accessed 21 Feb. 2025.
"""

from itertools import cycle
from itertools import islice
from datetime import datetime
from datetime import timedelta


DTBEGIN = datetime(1412, 1, 6)


# In the year 2525 If man is still alive If woman can survive They may find
DT2525 = datetime(2525, 1, 1)
# Put date in middle of month to avoid this issue during test:
#   https://github.com/scrapinghub/dateparser/issues/1266
I1266  = datetime(2525, 1, 20)

# In the year 3535 Ain't gonna need to tell the truth, tell no lies
# Everything you think, do, and say--Is in the pill you took today
DT3535 = datetime(3535, 1, 1)

# In the year 4545 Ain't gonna need your teeth; won't need your eyes
# You won't find a thing to chew--Nobody's gonna look at you
DT4545 = datetime(4545, 1, 1)

# In the year 5555 Your arms are hanging limp at your sides
# Your legs got nothing to do--Some machine's doing that for you
DT5555 = datetime(5555, 1, 1)

# In the year 6565 Ain't gonna need no husband; won't need no wife
# You'll pick your son, pick your daughter, too--From the bottom of a long glass tube
DT6565 = datetime(6565, 1, 1)

# In the year 7510 If God's a-comin', he oughta make it by then
# Maybe he'll look around Himself and say--Guess it's time for the Judgment day
DT7510 = datetime(7510, 1, 1)

# In the year 8510 God is gonna shake His mighty head
# He'll either say, "I'm pleased where man has been"--Or tear it down and start again
DT8510 = datetime(8510, 1, 1)

# In the year 9595 I'm kinda wonderin' if man is gonna be alive
DT9595 = datetime(9595, 1, 1)
# He's taken everything this old Earth can give--And he ain't put back nothin'
#
#     Now it's been ten thousand years
#     Man has cried a billion tears
#     For what he never knew
#     Now, man's reign is through
#
#     But through eternal night
#     The twinkling of starlight
#     So very far away
#     Maybe, it's only yesterday

# In the year 2525 If man is still alive; If woman can survive; They may thrive

# In the year 3535--Ain't gonna need to tell the truth...

YEAR2DT = {
    '2525':  DT2525,
    '3535':  DT3535,
    '4545':  DT4545,
    '5555':  DT5555,
    '6565':  DT6565,
    '7510':  DT7510,
    '8510':  DT8510,
    '9595':  DT9595,
}

def get_dt(yearstr, hour, minute=0, second=0, microsecond=0):
    """Get a datetime object with the specified time"""
    dt0 = YEAR2DT.get(yearstr, DTBEGIN)
    return datetime(
        dt0.year, dt0.month, dt0.day,
        hour=hour,
        minute=minute,
        second=second,
        microsecond=microsecond)

def get_iter_weekday(start_day, stopincl_day):
    """Get an iter that starts at one weekday and ends at another week day"""
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    idxa = weekdays.index(start_day)
    idxz = weekdays.index(stopincl_day) + 1
    if idxz < idxa:
        idxz += 7
    return islice(cycle(weekdays), idxa, idxz)

def hours2td(hours):
    """Get a timedelta object, given elapsed hours"""
    return timedelta(seconds=hours*3600)
