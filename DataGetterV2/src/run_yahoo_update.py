import json

from classes.YahooArticleGetter import YahooArticleGetter

########################################
# Create YahooArticleGetter
########################################
fb_config = json.load(open('../configs/facebook.json'))
tw_config = json.load(open('../configs/twitter.json'))

ya_getter = YahooArticleGetter(fb_config, tw_config)

# Update article share count. X ... posts from last X days.
ya_getter.update_article_shares(7)
