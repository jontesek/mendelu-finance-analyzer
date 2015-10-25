# Imports
from twython import Twython
import json
import pprint

# Oauth1: 
#TOKEN = '16544193-7WGWwdojggEwLKlAcDYT5aHrricmicbJLBteUvrsc'
#TOKEN_SECRET = 'afCjemeLZcYJpPgod8SZkYsSNykJwW9tlGkNJ1CfwFB93'
#twitter = Twython(APP_KEY, APP_SECRET, TOKEN, TOKEN_SECRET)

# Oauth2:
APP_KEY = 'YttP9JDT6Yh3NQmG2GGoVMRw7'
APP_SECRET = '0H9LNpJD5ig4AFtToo5lZspU8nimPMKz2qVcotrMd4485Rpo9V'
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

#limit = twitter.get_application_rate_limit_status()
#pprint.pprint(limit)

# Company profile
company = 'intelaxika'
#user_info = twitter.show_user(screen_name = company)
#print user_info

# Company timeline
try: 
    timeline = twitter.get_user_timeline(screen_name = company, count = 10)
except Exception, e:
    print e.error_code
    
result = twitter.search(q='to:DHGUDGIUO', lang = 'en', result_type = 'mixed', count = 100, since_id = 10)   
print result

#jfile = open("tw_inputs/intel_timeline.json")
#timeline = json.load(jfile)
#print len(timeline)
quit()
# Search company mentions
#mentions = twitter.search(q='@intel', lang = 'en', result_type = 'recent', count = 50)
# since_id = 25450000000    od tohoto ID hledat
jfile = open("tw_inputs/intel_mentions.json")
mentions = json.load(jfile)

#for status in mentions['statuses']:
#    print status['id_str'] + ": " + status['text'].strip()

# Search company name
#searches = twitter.search(q='#amd', lang = 'en', result_type = 'recent', count = 50)
jfile = open("tw_inputs/intel_searches.json")
searches = json.load(jfile)

for status in searches['statuses']:
    print status['id_str'] + ": " + status['text'].strip()


