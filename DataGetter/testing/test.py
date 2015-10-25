import re

# URL
native_url = 'http://finance.yahoo.com/news/amd-showcases-jagex-gaming-studios-130000939.html'
external_url = 'http://us.rd.yahoo.com/finance/external/tsmfe/SIG=13epapkbf/*http://www.thestreet.com/story/13038609/1/one-reason-advanced-micro-devices-amd-stock-closed-down-today.html?puc=yahoo&cm_ven=YAHOO'

native_p = re.compile('^http://finance.yahoo.com/news/.+')

m = native_p.match(external_url)

error_code = 100

if error_code not in [100, 1, -3]:
    print "serious"

import datetime

print int(datetime.datetime.time())