import json

import facebook

from classes.FacebookGetter import FacebookGetter

########################################
# FB config
########################################

fb_config = json.load(open('../configs/facebook.json'))
#ACCES_TOKEN = facebook.get_app_access_token(APP_ID, APP_SECRET)

########################################
# Create FacebookGetter
########################################
fb_api = facebook.GraphAPI(fb_config['access_token'], version='2.7')
fb_getter = FacebookGetter(fb_api)

# update post and comments stats. X ... posts from last X days.
fb_getter.update_posts(14)
