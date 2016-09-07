########################################
# Imports
########################################
from classes.YahooArticleGetter import YahooArticleGetter


########################################
# Create YahooArticleGetter 
########################################
ya_getter = YahooArticleGetter()

# Update article stats. X ... posts from last X days.
ya_getter.update_article_stats(14)
