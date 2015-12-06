import os
import datetime
import re

import nltk

from StockPriceProcessor import StockPriceProcessor
from TextProcessorDbModel import TextProcessorDbModel
from TextWriter import TextWriter


class TextProcessor(object):

    def __init__(self, file_paths):
        # DB model
        self.dbmodel = TextProcessorDbModel()
        # Path to input and output dirs
        self.file_paths = file_paths
        # self.stop_words = self._read_stopwords(file_paths['stopwords'])
        # Object for stock movements
        self.stock_processor = StockPriceProcessor()
        # Regexp patterns
        self.pattern_http = re.compile('https?:\/\/.* ')
        # Object for writing text files
        self.text_writer = TextWriter(os.path.abspath(file_paths['output_dir']))
        # Output file - document count variables
        self.documents_count = 0
        self.documents_per_file = 50000
        self.files_count = 1

    # MAIN PROCESSING

    def process_articles_for_company(self, company_id):
        articles = self.dbmodel.get_articles_for_company(company_id)
        print articles.fetchone()

    def process_fb_posts_for_company(self, company_id, from_date, days_delay, total_file_name=False):
        # Set stock movements
        self.stock_processor.set_stock_movements(company_id, from_date)
        # Get posts from DB
        fb_posts = self.dbmodel.get_fb_posts_for_company(company_id, from_date)
        # Process posts and create a list for writing to a file.
        new_posts_list = []
        for post in fb_posts:
            # print post['id'],
            # Get existing data for price lookup
            post_date = datetime.datetime.utcfromtimestamp(post['created_timestamp']).date()
            working_date = self.stock_processor.create_lookup_and_find_working_date(post_date, days_delay)
            # If the company was not on the stock exchange on this date, skip the post.
            if not working_date:
                continue
            # Increment current file's documents count
            self.documents_count += 1
            # Get stock price movement direction
            movement_direction = self.stock_processor.get_stock_direction(working_date)
            # Edit document text
            post_text = self._process_facebook_text(post['text'])
            # Add selected data to the list.
            new_list = [movement_direction, post_text]
            new_posts_list.append(new_list)
        # Choose the correct file name (bulk vs individual generating).
        if total_file_name:
            file_name = total_file_name
            file_mode = 'a'
        else:
            file_name = 'fb_post_%s_%s_%s' % (company_id, from_date.strftime('%Y-%m-%d'), str(days_delay))
            file_mode = 'w'
        # Write data to the file
        self.text_writer.write_file_for_vectorization(file_name, new_posts_list, file_mode)

    def process_all_fb_posts(self, from_date, days_delay):
        # Create file name
        file_name = 'fb_posts_all_%s_%s' % (from_date.strftime('%Y-%m-%d'), str(days_delay))
        # Remove old file with the same name.
        # os.remove('%s/%s.%s' % (self.file_paths['output_dir'], file_name, 'txt'))
        # Process all companies
        for comp in self.dbmodel.get_companies():
            print('===Company %d===') % comp[0]
            # Check if the file should be ended.
            if self.documents_count > self.documents_per_file:
                print('>>>NEW FILE')
                self.files_count += 1
                self.documents_count = 0
                file_name += '_' + str(self.files_count)
            # Process and write data for one company.
            self.process_fb_posts_for_company(comp[0], from_date, days_delay, file_name)

    def _process_facebook_text(self, text):
        # Remove whitespace
        text = ' '.join(text.strip().split())
        # Remove hyper links
        text = re.sub('https?:\/\/.* ?', '', text)
        # Remove hash tags - but they are sometimes parts of a sentence. -> remove the last occurence???
        # Lowercase the text
        # text = unicode(text, 'utf-8').lower()
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