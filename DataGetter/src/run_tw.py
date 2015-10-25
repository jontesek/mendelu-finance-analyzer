########################################
# Imports
########################################
from twython import Twython
from classes.TwitterGetter import TwitterGetter

########################################
# Twitter config 
########################################
APP_KEY = 'YttP9JDT6Yh3NQmG2GGoVMRw7'
APP_SECRET = '0H9LNpJD5ig4AFtToo5lZspU8nimPMKz2qVcotrMd4485Rpo9V'
twitter_api = Twython(APP_KEY, APP_SECRET, oauth_version=2)
#ACCESS_TOKEN = twitter_api.obtain_access_token()
ACCESS_TOKEN = 'AAAAAAAAAAAAAAAAAAAAANczfQAAAAAAUiCzh70Gj7F61%2FTRcDJiqhGh4iY%3DFJSOFkkMfTey5RxFjQlx2ZKCbn3bVnEhZ4RL7LmHajiAKM3xhc'
twitter_api = Twython(APP_KEY, access_token=ACCESS_TOKEN)

########################################
# Create TwitterGetter 
########################################
tw_getter = TwitterGetter(twitter_api)

tw_getter.get_all_tweets()
