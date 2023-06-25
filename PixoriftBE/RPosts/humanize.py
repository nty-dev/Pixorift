from datetime import datetime, timedelta
import pytz

def monthdiff(d1, d2):
    yeardiff = d1.year - d2.year
    if yeardiff < 0:
        return "Order of dates is wrong!"
    if yeardiff == 0:
        return d1.month - d2.month
    if yeardiff > 0:
        extramonths = yeardiff * 12
        return extramonths + d1.month - d2.month

def humanize(dt):
    tnow = datetime.utcnow().replace(tzinfo=pytz.utc)
    td = tnow - dt
    if td.seconds < 60:
        if td.seconds == 1:
            return str(td.seconds) + " second ago."
        else:
            return str(td.seconds) + " seconds ago."
    elif td.seconds < 3600:
        if int(td.seconds/60) == 1:
            return str(int(td.seconds/60)) + " minute ago."
        else:
            return str(int(td.seconds/60)) + " minutes ago."
    elif td.days == 0:
        if int(td.seconds/3600) == 1:
            return str(int(td.seconds/3600)) + " hour ago."
        else:
            return str(int(td.seconds/3600)) + " hours ago."
    elif td.days < 7:
        if td.days == 1:
            return str(td.days) + " day ago."
        else:
            return str(td.days) + " days ago."
    elif monthdiff(tnow, dt) == 0:
        if int(td.days/7) == 1:
            return str(int(td.days/7)) + " week ago."
        else:
            return str(int(td.days/7)) + " weeks ago."
    elif tnow.year - dt.year == 0:
        if monthdiff(tnow, dt) == 1:
            return str(monthdiff(tnow, dt)) + " month ago."
        else:
            return str(monthdiff(tnow, dt)) + " months ago."
    else:
        if tnow.year - dt.year == 1:
            return str(tnow.year - dt.year) + " year ago."
        else:
            return str(tnow.year - dt.year) + " years ago."
