import datetime
import time

dt = datetime.datetime(2015,10,15,0,0,0)

print long(time.mktime(dt.timetuple()))

unix = 1444860000
dt = datetime.datetime.utcfromtimestamp(unix)
print dt

