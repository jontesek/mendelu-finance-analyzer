import json
import datetime
import os.path

from twython import Twython

from classes.TwitterGetter import TwitterGetter

os.chdir(os.path.dirname(os.path.abspath(__file__)))

########################################
# Twitter config 
########################################
tw_config = json.load(open('../configs/twitter.json'))

#twitter_api = Twython(tw_config['app_key'], tw_config['app_secret'], oauth_version=2)
#ACCESS_TOKEN = twitter_api.obtain_access_token()
twitter_api = Twython(app_key=tw_config['app_key'], access_token=tw_config['access_token'])

########################################
# Create TwitterGetter 
########################################
tw_getter = TwitterGetter(twitter_api)

# Get all tweets
start_time = datetime.datetime.now()
tw_getter.get_all_tweets()
end_time = datetime.datetime.now()

# Log execution
script_name = os.path.basename(__file__).replace('.py', '')
duration = end_time - start_time
tw_getter.db_model.add_log_exec(script_name, tw_getter.exec_error, start_time, end_time, duration)
print('>>>>Script duration: {0}'.format(str(duration)))
