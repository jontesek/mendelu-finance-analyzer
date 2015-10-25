import os
import datetime
import nltk
from TextProcessorDbModel import TextProcessorDbModel


class TextProcessor(object):

    def __init__(self, file_paths):
        self.dbmodel = TextProcessorDbModel()
        #self.stop_words = self._read_stopwords(file_paths['stopwords'])
        self.stock_movements = {'company_id': None, 'prices': {}}

    # MAIN PROCESSING

    def process_articles_for_company(self, company_id):
        articles = self.dbmodel.get_articles_for_company(company_id)
        print articles.fetchone()

    def process_fb_posts_for_company(self, company_id, from_date):
        fb_posts = self.dbmodel.get_fb_posts_for_company(company_id, from_date)
        new_post_list = []
        for post in fb_posts:
            print post['id'],
            post_date = datetime.datetime.utcfromtimestamp(post['created_timestamp']).date()
            lookup_date = post_date + datetime.timedelta(days=1)
            print lookup_date,
            price_movement = self.stock_movements['prices'][lookup_date]
            print price_movement
            pass# Convert timestamp to date and text to lowercase
            # Remove stop words

    def get_stock_movements(self, company_id, from_date):
        """Get relative stock movement for days from given date to present day.

        Args:
            company_id (int): Company ID
            from_date (Datetime): from which date to search (also two previous days will be saved)

        Returns:
            list: (datetime, float): stock price movements as percentage change (current/last day)
        """
        # Substract three days to be sure to get data for the from_date.
        early_from_date = from_date - datetime.timedelta(days=3)
        # Get stock prices for individual dates
        stock_prices = self.dbmodel.get_stock_prices(company_id, early_from_date)
        # Create stock price movements for the dates
        for index, (price_date, price) in enumerate(stock_prices):
            if index == 0:
                continue
            ratio = (price / stock_prices[index - 1][1]) - 1
            self.stock_movements['prices'][price_date] = ratio*100
        # return list
        self.stock_movements['company_id'] = company_id
        print self.stock_movements



    # STOP WORDS
    def remove_stop_words(self, input_string):
        tokens = nltk.word_tokenize(input_string.lower())
        ok_words = [word for word in tokens if word not in self.stop_words]
        print ' '.join(ok_words)

    def _read_stopwords(self, filepath):
        abs_path = os.path.abspath(filepath)
        with open(abs_path) as f:
            return set(f.read().split('\n'))