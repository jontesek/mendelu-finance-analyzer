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
#ACCES_TOKEN = facebook.get_app_access_token(APP_ID, APP_SECRET)
ACCES_TOKEN = '169550103254801|IYXMyBn0MiDMtqrRiO-OkjFauiw'

########################################
# Create FacebookGetter
########################################
fb_api = facebook.GraphAPI(ACCES_TOKEN)
fb_getter = FacebookGetter(fb_api)

# Save new posts to database
fb_getter.get_new_posts()

