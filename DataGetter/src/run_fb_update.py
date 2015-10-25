########################################
# Imports
########################################
import facebook
from classes.FacebookGetter import FacebookGetter

########################################
# FB config
########################################
APP_ID = '169550103254801'
APP_SECRET = '2ec0d363d00345ef25e6a2e0a64a4d27'
#ACCESS_TOKEN = facebook.get_app_access_token(APP_ID, APP_SECRET)
ACCESS_TOKEN = '169550103254801|IYXMyBn0MiDMtqrRiO-OkjFauiw'

########################################
# Create FacebookGetter
########################################
fb_api = facebook.GraphAPI(ACCESS_TOKEN)
fb_getter = FacebookGetter(fb_api)

# update post and comments stats. X ... posts from last X days.
fb_getter.update_posts(14)
