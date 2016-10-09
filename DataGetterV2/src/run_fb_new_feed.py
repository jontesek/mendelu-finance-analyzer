import json

import facebook

from classes.FacebookGetter import FacebookGetter

########################################
# FB config
########################################

fb_config = json.load(open('../configs/facebook.json'))

########################################
# Create FacebookGetter
########################################
fb_api = facebook.GraphAPI(fb_config['access_token'], version='2.7')
fb_getter = FacebookGetter(fb_api)

# Save new posts to database
fb_getter.get_new_feed_items()
