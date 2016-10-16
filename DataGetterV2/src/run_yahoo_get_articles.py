import datetime
import json

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

ya_getter.get_new_articles((0, 0))
