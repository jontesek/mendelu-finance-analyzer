########################################
# Imports
########################################
import datetime

from classes.YahooArticleGetter import YahooArticleGetter


########################################
# Create YahooArticleGetter 
########################################
ya_getter = YahooArticleGetter()

ya_getter.get_headlines('MSFT', 300, datetime.datetime(2016, 8, 3, 0, 0, 0))
#ya_getter.get_headlines('ABBV', 3, datetime.datetime(2016, 9, 8, 20, 4, 45))
#ya_getter.get_headlines('BMY', 73, datetime.datetime(2016, 1, 3, 0, 0, 0))

#ya_getter.get_new_articles()
