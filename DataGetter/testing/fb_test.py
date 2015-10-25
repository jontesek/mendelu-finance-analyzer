########################################
# Imports
########################################
import facebook


########################################
# FB config
########################################
APP_ID = '169550103254801'
APP_SECRET = '2ec0d363d00345ef25e6a2e0a64a4d27'
#token = facebook.get_app_access_token(APP_ID, APP_SECRET)
access_token = '169550103254801|IYXMyBn0MiDMtqrRiO-OkjFauiw'

########################################
# Create FacebookGetter
########################################
fb_api = facebook.GraphAPI(access_token)

try:
    my_fields='id,created_time,message,shares,likes.limit(0).summary(true),comments.limit(25).summary(true)'
    result =fb_api.get_connections(id='citi', connection_name = 'posts', limit=250, date_format='U', fields=my_fields)
except Exception, e:
    print e.result
    print e.result['error']['code']