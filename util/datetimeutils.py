from datetime import datetime,timedelta

def days_ago(days = 0, now = datetime.now()) :
    start = datetime.min.replace(year = now.year, month = now.month, day = now.day)
    return (start - timedelta(days))


def begining_of_the_day(now = datetime.now()) :
    return datetime.min.replace(year = now.year, month = now.month, day = now.day)


def days_ago_not_before(days = 0, now = datetime.now(), not_before_date = None) :
    ago = days_ago(days, now)
    if ago < not_before_date :
        return not_before_date
    else :
        return ago

