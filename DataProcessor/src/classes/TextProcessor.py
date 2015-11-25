import os
import datetime
import re

import nltk

from TextProcessorDbModel import TextProcessorDbModel
from TextWriter import TextWriter


class TextProcessor(object):

    def __init__(self, file_paths = {'output'}):
        self.dbmodel = TextProcessorDbModel()
        self.file_paths = file_paths
        #self.stop_words = self._read_stopwords(file_paths['stopwords'])
        self.stock_movements = {'company_id': None, 'ratios': {}}
        # regexp patterns
        self.pattern_http = re.compile('https?:\/\/.* ')
        self.const_boundaries = (-0.5,0.5)
        # writing text files
        self.text_writer = TextWriter(os.path.abspath(file_paths['output_dir']))

    # MAIN PROCESSING

    def process_articles_for_company(self, company_id):
        articles = self.dbmodel.get_articles_for_company(company_id)
        print articles.fetchone()

    def process_fb_posts_for_company(self, company_id, from_date, days_delay):
        # Get posts from DB
        fb_posts = self.dbmodel.get_fb_posts_for_company(company_id, from_date)
        # Process posts and create a list for writing to a file
        new_posts_list = []
        for post in fb_posts:
            #print post['id'],
            # Get price movement
            post_date = datetime.datetime.utcfromtimestamp(post['created_timestamp']).date()
            lookup_date = post_date + datetime.timedelta(days=days_delay)
            working_date = self._get_working_date(lookup_date)
            price_movement = self.stock_movements['ratios'][working_date]
            movement_direction = self._format_stock_movement(price_movement, self.const_boundaries)
            # Edit text
            post_text = self._process_facebook_text(post['text'])
            # Add selected data to the list.
            new_list = [movement_direction, post_text]
            new_posts_list.append(new_list)
            #print new_list
        # Send the data to TextWriter object.
        file_name = 'fb_post_%s_%s_%s' % (company_id, from_date.strftime('%Y-%m-%d'), str(days_delay))
        self.text_writer.write_file_for_vectorization(file_name, new_posts_list)

    def set_stock_movements(self, company_id, from_date):
        """Get relative stock movement for days from given date to present day.

        Args:
            company_id (int): Company ID
            from_date (Datetime): from which date to search (also 3 previous days will be saved)

        Returns:
            list: (datetime, float): stock price movements as percentage change (current/last day)
        """
        # Substract 3 days to be sure to get data for the from_date.
        from_date = from_date.date()
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

    def _format_stock_movement(self, percentage_change, const_boundaries):
        """Get string representation of a size of stock movement.

        :param percentage_change: percentage change
        :type float
        :param const_boundaries: [min, max] for constant state
        :return: direction
        """
        if const_boundaries[0] < percentage_change < const_boundaries[1]:
            return 'const'
        if percentage_change > 0:
            return 'up'
        elif percentage_change < 0:
            return 'down'
        else:
            return 'const'

    def _get_working_date(self, lookup_date):
        """Gheck if given date is a working day. If not, return minus one or minus two days date.

        Args:
            lookup_date (Datetime)

        Returns:
            Datetime: the same date or date of the previous working day
        """
        # For working day
        if lookup_date in self.stock_movements['ratios']:
            return lookup_date
        # Search past working date
        search_past_days = 14
        for i in range(1, search_past_days):
            date_minus = lookup_date - datetime.timedelta(days=i)
            if date_minus in self.stock_movements['ratios']:
                return date_minus
        # nothing found
        return False


    def _process_facebook_text(self, text):
        # Remove whitespace
        text = ' '.join(text.strip().split())
        # Remove hyper links
        text = re.sub('https?:\/\/.* ?', '', text)
        # Remove hash tags - but they are sometimes parts of a sentence. -> remove the last occurence???
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