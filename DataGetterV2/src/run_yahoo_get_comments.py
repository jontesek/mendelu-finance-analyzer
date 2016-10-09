import datetime

from classes.YahooArticleGetter import YahooArticleGetter


ya_getter = YahooArticleGetter()

ya_getter.get_article_comments(10, 1)
