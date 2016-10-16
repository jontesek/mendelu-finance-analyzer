import json
import datetime
import os.path

from classes.YahooArticleGetter import YahooArticleGetter

########################################
# Create YahooArticleGetter
########################################
fb_config = json.load(open('../configs/facebook.json'))
tw_config = json.load(open('../configs/twitter.json'))

ya_getter = YahooArticleGetter(fb_config, tw_config)

# Get new comments and save comment history for articles from last X days.
start_time = datetime.datetime.now()
ya_getter.get_article_comments(7)
end_time = datetime.datetime.now()

# Log execution
script_name = os.path.basename(__file__).replace('.py', '')
duration = end_time - start_time
ya_getter.db_model.add_log_exec(script_name, ya_getter.exec_error, start_time, end_time, duration)

print('>>>>Script duration: {0}'.format(str(duration)))
