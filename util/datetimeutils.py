from datetime import datetime,timedelta
import re

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

def to_unix_timestamp(day_of_start):
    epoch = int(day_of_start.strftime('%s'))
    usec = day_of_start.microsecond
    return epoch + (usec / 1000000.0)

def cctimestamp_to_unix_timestamp(cctimestamp) :
    ccdate = datetime.strptime(cctimestamp, "%Y%m%d%H%M%S")
    return to_unix_timestamp(ccdate)

def evaluate_time_to_seconds(time_str) :
    left = re.compile('\(')
    right = re.compile('\)')
    second = re.compile('second')
    minute = re.compile('minute')
    hour = re.compile('hour')
    s = re.compile('s')
    trailing_plus = re.compile('\+$')
    result = s.sub('', hour.sub("*3600 + ",  minute.sub('*60 + ', second.sub( '', time_str))))
    result = trailing_plus.sub('', result)
    result = right.sub('', left.sub('', result))
    return eval(str(result))


