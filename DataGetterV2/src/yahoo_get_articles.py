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

#ya_getter.get_headlines('MSFT', 300, datetime.datetime(2016, 9, 9, 14, 4, 21))
#ya_getter.get_headlines('ABBV', 3, datetime.datetime(2016, 9, 8, 20, 4, 45))
#ya_getter.get_headlines('BOSS.DE', 636, datetime.datetime(2016, 8, 3, 0, 0, 0))

# Get new articles
start_time = datetime.datetime.now()
ya_getter.get_new_articles((0, 0))
end_time = datetime.datetime.now()

# Log execution
script_name = os.path.basename(__file__).replace('.py', '')
duration = end_time - start_time
ya_getter.db_model.add_log_exec(script_name, ya_getter.exec_error, start_time, end_time, duration)
print('>>>>Script duration: {0}'.format(str(duration)))
