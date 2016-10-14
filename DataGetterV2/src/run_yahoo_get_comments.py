import json

from classes.YahooArticleGetter import YahooArticleGetter

########################################
# Create YahooArticleGetter
########################################
fb_config = json.load(open('../configs/facebook.json'))
tw_config = json.load(open('../configs/twitter.json'))

ya_getter = YahooArticleGetter(fb_config, tw_config)

ya_getter.get_article_comments(10, 1)
