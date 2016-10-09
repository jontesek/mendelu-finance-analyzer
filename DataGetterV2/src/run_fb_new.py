import json

import facebook

from classes.FacebookGetter import FacebookGetter

########################################
# FB config
########################################

fb_config = json.load(open('../configs/facebook.json'))
#fb_api = facebook.GraphAPI()
#ACCES_TOKEN = fb_api.get_app_access_token(fb_config['app_id'], fb_config['app_secret'])

########################################
# Create FacebookGetter
########################################
fb_api = facebook.GraphAPI(fb_config['access_token'], version='2.7')
fb_getter = FacebookGetter(fb_api)

# Save new posts to database
fb_getter.get_new_posts()
