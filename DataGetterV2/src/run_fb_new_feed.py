import json
import datetime
import os.path

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

# Save items from page feed (including visitors wall posts)
start_time = datetime.datetime.now()
fb_getter.get_new_feed_items()
end_time = datetime.datetime.now()

# Log execution
script_name = os.path.basename(__file__).replace('.py', '')
duration = end_time - start_time
fb_getter.db_model.add_log_exec(script_name, fb_getter.exec_error, start_time, end_time, duration)
print('>>>>Script duration: {0}'.format(str(duration)))
