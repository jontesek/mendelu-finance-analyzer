import time
import datetime
import re
import pytz

# Current timestamp
timestamp = int(time.time())


####Last 2 days
h_date = datetime.datetime(2015, 7, 17)
max_date = h_date - datetime.timedelta(days=2)
#print max_date

#print datetime.datetime.utcnow().date()
#convert to edt
ny_tz = pytz.timezone('America/New_York')
utc_time = pytz.utc.localize(datetime.datetime.utcnow())
edt_time = utc_time.astimezone(ny_tz).date()
#print utc_time
#print datetime.datetime.now(pytz.timezone('America/New_York'))
#print datetime.datetime.now(pytz.timezone('America/New_York')).replace(minute=0, hour=0, second=0, microsecond=0)

#print datetime.date.today().datetime()

#### daylight saving
# http://stackoverflow.com/questions/19774709/use-python-to-find-out-if-a-timezone-currently-in-daylight-savings-time
#tz = pytz.timezone('America/New_York')
tz = pytz.timezone('Europe/Prague')
now = pytz.utc.localize(datetime.datetime.utcnow())
#print now.astimezone(tz).dst() != datetime.timedelta(0)

# Convert given time to UTC
ny_tz = pytz.timezone('America/New_York')
ny_time = ny_tz.localize(datetime.datetime(2015, 7, 17, 10, 10))
utc_time = ny_time.astimezone(pytz.UTC)

### article time hour
article_time_string = 'Fri 1:10PM EDT'
at_p = re.compile('\w+ (\d+:\d+\w\w) .*')
at_match = at_p.match(article_time_string)
#print at_match.group(1)
article_time = datetime.datetime.strptime(at_match.group(1), '%I:%M%p')
article_datetime = datetime.datetime(2015, 7, 17) + datetime.timedelta(hours=article_time.hour) + datetime.timedelta(minutes=article_time.minute)
#print article_datetime


#### article time

# server time 
server_string = 'Fri, Jul 17, 2015, 8:08AM EDT - US Markets open in 1 hr and 3 mins'
server_time_exp = re.compile('\w+, (\w+) (\d+), (\d{4}), (\d+:\d+\w\w) (\w+) .*') 
s_time = server_time_exp.match(server_string)
server_time_string = '%s %s, %s, %s' % (s_time.group(1), s_time.group(2), s_time.group(3), s_time.group(4)) 
if s_time.group(5) == 'EDT':
    utc_offset = 4
else:
    utc_offset = 5

s_time_object = datetime.datetime.strptime(server_time_string, '%b %d, %Y, %I:%M%p')
server_time_o = s_time_object + datetime.timedelta(hours=utc_offset)
#print s_time_object
#print server_time_o

# Article time

article_ago = '10 hours ago'
ago_rexp = re.compile('(\d+) (\w+) ago')
result = ago_rexp.match(article_ago)
time_n = long(result.group(1))

if result.group(2) == 'minutes':
    article_time = server_time_o - datetime.timedelta(minutes=time_n)
else:
    article_time = server_time_o - datetime.timedelta(hours=time_n)
    
#print article_time




### OLD

# Date to timestamp
dt = datetime.datetime(2015,6,22,11,59,52)
#print dt
ts = int(time.mktime(dt.timetuple()))
#print ts
ts = dt.strftime("%s")
print ts

fb_date = '2015-06-22T11:59:52+0000'        # realne 13:59 v cr
fb_timestamp = 1434974392

# Timestamp to date
ndt = datetime.datetime.fromtimestamp(fb_timestamp)
#print fb_timestamp

# String to date
# http://stackoverflow.com/questions/466345/converting-string-into-datetime


date_string= 'Thursday, February 19, 2015'
p = re.compile('\w+, (\w+) (\d+), (\d+)')
m = p.match(date_string)


date_object = datetime.datetime.strptime(date_string, '%A, %B %d, %Y')
#print date_object

datetime_string = 'Wed Aug 29 17:12:58 +0000 2012'
datetime_object = datetime.datetime.strptime(datetime_string, '%a %b %d %H:%M:%S +0000 %Y')
#print datetime_object



