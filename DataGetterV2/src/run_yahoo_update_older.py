import json

from classes.YahooArticleGetter import YahooArticleGetter

########################################
# Create YahooArticleGetter
########################################
fb_config = json.load(open('../configs/facebook.json'))
tw_config = json.load(open('../configs/twitter.json'))

ya_getter = YahooArticleGetter(fb_config, tw_config)

# Update article stats for articles published from 7 to 2 days ago
ya_getter.update_article_stats(7, (7, 2))
