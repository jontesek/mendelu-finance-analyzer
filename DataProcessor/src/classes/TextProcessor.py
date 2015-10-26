import os
import datetime
import nltk
from TextProcessorDbModel import TextProcessorDbModel


class TextProcessor(object):

    def __init__(self, file_paths):
        self.dbmodel = TextProcessorDbModel()
        #self.stop_words = self._read_stopwords(file_paths['stopwords'])
        self.stock_movements = {'company_id': None, 'ratios': {}}

    # MAIN PROCESSING

    def process_articles_for_company(self, company_id):
        articles = self.dbmodel.get_articles_for_company(company_id)
        print articles.fetchone()

    def process_fb_posts_for_company(self, company_id, from_date, days_delay):
        fb_posts = self.dbmodel.get_fb_posts_for_company(company_id, from_date)
        new_post_list = []
        for post in fb_posts:
            print post['id'],
            # Get price movement
            post_date = datetime.datetime.utcfromtimestamp(post['created_timestamp']).date()
            lookup_date = post_date + datetime.timedelta(days=days_delay)
            working_date = self._get_working_date(lookup_date)
            print lookup_date, working_date,
            price_movement = self.stock_movements['ratios'][working_date]
            print price_movement,
            # Edit text
            post_text = self._process_facebook_text(post['text'])
            print post_text

    def set_stock_movements(self, company_id, from_date):
        """Get relative stock movement for days from given date to present day.

        Args:
            company_id (int): Company ID
            from_date (Datetime): from which date to search (also 3 previous days will be saved)

        Returns:
            list: (datetime, float): stock price movements as percentage change (current/last day)
        """
        # Substract 3 days to be sure to get data for the from_date.
        early_from_date = from_date - datetime.timedelta(days=3)
        # Get stock prices for individual dates
        stock_prices = self.dbmodel.get_stock_prices(company_id, early_from_date)
        # Create stock price movements for the dates
        for index, (price_date, price) in enumerate(stock_prices):
            if index == 0:
                continue
            ratio = (price / stock_prices[index - 1][1]) - 1
            self.stock_movements['ratios'][price_date] = ratio*100
        # return list
        self.stock_movements['company_id'] = company_id
        print self.stock_movements

    def _get_working_date(self, lookup_date):
        """Gheck if given date is a working day. If not, return minus one or minus two days date.

        Args:
            lookup_date (Datetime)

        Returns:
            Datetime: the same date or date of the previous working day
        """
        if lookup_date in self.stock_movements['ratios']:
            return lookup_date
        date_minus_1 = lookup_date - datetime.timedelta(days=1)
        if date_minus_1 in self.stock_movements['ratios']:
            return date_minus_1
        date_minus_2 = lookup_date - datetime.timedelta(days=2)
        if date_minus_2 in self.stock_movements['ratios']:
            return date_minus_2


    def _process_facebook_text(self, text):
        # Remove whitespace
        text = ' '.join(text.strip().split())
        # Remove hyper links - regexp
        
        # Lowercase the text
        #text = unicode(text,'utf-8').lower()
        text = text.lower()

        return text



    # STOP WORDS
    def remove_stop_words(self, input_string):
        tokens = nltk.word_tokenize(input_string.lower())
        ok_words = [word for word in tokens if word not in self.stop_words]
        print ' '.join(ok_words)

    def _read_stopwords(self, filepath):
        abs_path = os.path.abspath(filepath)
        with open(abs_path) as f:
            return set(f.read().split('\n'))