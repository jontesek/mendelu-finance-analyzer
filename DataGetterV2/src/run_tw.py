import json

from twython import Twython

from classes.TwitterGetter import TwitterGetter

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

tw_getter.get_all_tweets(15)
