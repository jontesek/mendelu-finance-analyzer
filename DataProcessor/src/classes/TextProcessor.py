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
        self.db_model = TextProcessorDbModel()
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

    def process_articles_for_company(self, company_id, from_date, days_delay, total_file_name=False):
        # Set stock movements
        self.stock_processor.set_stock_prices(company_id, from_date)
        # Get posts from DB
        articles = self.db_model.get_articles_for_company(company_id, from_date)
        # Process posts and create a list for writing to a file.
        new_articles_list = []
        for article in articles:
            # Get existing data for price lookup
            article_date = article['published_date'].date()
            working_date = self.stock_processor.create_lookup_and_find_working_date(article_date, days_delay)
            # If the company was not on the stock exchange on this date, skip the post.
            if not working_date:
                continue
            # Get stock price movement direction
            movement_direction = self.stock_processor.get_stock_direction(working_date)
            # Skip constant direction
            if movement_direction == 'const':
                continue
            # Edit document text
            article_text = self._process_article_text(article['text'])
            # Add selected data to the list.
            new_list = [movement_direction, article_text]
            new_articles_list.append(new_list)
            # Increment current file's documents count.
            self.documents_count += 1
        # Choose the correct file name (bulk vs individual generating).
        if total_file_name:
            file_name = total_file_name
            file_mode = 'a'
        else:
            file_name = 'article_%s_%s_%s' % (company_id, from_date.strftime('%Y-%m-%d'), str(days_delay))
            file_mode = 'w'
        # Write data to the file
        self.text_writer.write_file_for_vectorization(file_name, new_articles_list, file_mode)

    def process_all_articles(self, from_date, days_delay):
        # Create file name
        file_name = 'articles_all_%s_%s' % (from_date.strftime('%Y-%m-%d'), str(days_delay))
        # Remove old file with the same name.
        # os.remove('%s/%s.%s' % (self.file_paths['output_dir'], file_name, 'txt'))
        # Process all companies
        for comp in self.db_model.get_companies():
            print('===Company %d===') % comp[0]
            # Check if the file should be ended.
            if self.documents_count > self.documents_per_file:
                print('>>>NEW FILE')
                self.files_count += 1
                self.documents_count = 0
                file_name += '_' + str(self.files_count)
            # Process and write data for one company.
            self.process_articles_for_company(comp[0], from_date, days_delay, file_name)

    def process_fb_comments_for_company(self, company_id, from_date, days_delay, total_file_name=False):
        # Set stock movements
        self.stock_processor.set_stock_prices(company_id, from_date)
        # Get posts from DB
        fb_comments = self.db_model.get_fb_comments_for_company(company_id, from_date)
        # Process posts and create a list for writing to a file.
        new_comments_list = []
        for comment in fb_comments:
            # Get existing data for price lookup
            post_date = datetime.datetime.utcfromtimestamp(comment['created_timestamp']).date()
            working_date = self.stock_processor.create_lookup_and_find_working_date(post_date, days_delay)
            # If the company was not on the stock exchange on this date, skip the post.
            if not working_date:
                continue
            # Get stock price movement direction
            movement_direction = self.stock_processor.get_stock_direction(working_date)
            # Skip constant direction
            if movement_direction == 'const':
                continue
            # Edit document text
            post_text = self._process_facebook_text(comment['text'])
            # Add selected data to the list.
            new_list = [movement_direction, post_text]
            new_comments_list.append(new_list)
            # Increment current file's documents count.
            self.documents_count += 1
        # Choose the correct file name (bulk vs individual generating).
        if total_file_name:
            file_name = total_file_name
            file_mode = 'a'
        else:
            file_name = 'fb_comment_%s_%s_%s' % (company_id, from_date.strftime('%Y-%m-%d'), str(days_delay))
            file_mode = 'w'
        # Write data to the file
        self.text_writer.write_file_for_vectorization(file_name, new_comments_list, file_mode)

    def process_all_fb_comments(self, from_date, days_delay):
        # Create file name
        file_name = 'fb_comments_all_%s_%s' % (from_date.strftime('%Y-%m-%d'), str(days_delay))
        # Remove old file with the same name.
        # os.remove('%s/%s.%s' % (self.file_paths['output_dir'], file_name, 'txt'))
        # Process all companies
        for comp in self.db_model.get_companies():
            print('===Company %d===') % comp[0]
            # Check if the file should be ended.
            if self.documents_count > self.documents_per_file:
                print('>>>NEW FILE')
                self.files_count += 1
                self.documents_count = 0
                file_name += '_' + str(self.files_count)
            # Process and write data for one company.
            self.process_fb_comments_for_company(comp[0], from_date, days_delay, file_name)

    def process_fb_posts_for_company(self, company_id, from_date, days_delay, total_file_name=False):
        # Set stock prices for given company
        prices = self.stock_processor.set_stock_prices(company_id, from_date)
        if not prices:
            return False
        # Get posts from DB
        fb_posts = self.db_model.get_fb_posts_for_company(company_id, from_date)
        # Process posts and create a list for writing to a file.
        new_posts_list = []
        for post in fb_posts:
            # print post['id'],
            # Get document publication date
            post_date = datetime.datetime.utcfromtimestamp(post['created_timestamp']).date()
            # Get stock price movement direction
            movement_direction = self.stock_processor.get_price_movement_with_delay(post_date, days_delay)
            # If the company was not on the stock exchange on this date, skip the post.
            if not movement_direction:
                continue
            # Skip constant direction
            if movement_direction == 'const':
                continue
            # Edit document text
            post_text = self._process_facebook_text(post['text'])
            # Add selected data to the list.
            new_list = [movement_direction, post_text]
            new_posts_list.append(new_list)
            # Increment current file's documents count
            self.documents_count += 1
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
        for comp in self.db_model.get_companies():
            print('===Company %d===') % comp[0]
            # Check if the file should be ended.
            if self.documents_count > self.documents_per_file:
                print('>>>NEW FILE')
                self.files_count += 1
                self.documents_count = 0
                file_name += '-' + str(self.files_count)
            # Process and write data for one company.
            self.process_fb_posts_for_company(comp[0], from_date, days_delay, file_name)

    def _process_facebook_text(self, text):
        # Remove whitespace
        text = ' '.join(text.strip().split())
        # Remove hyper links
        text = re.sub('https?:\/\/.* ?', '', text)
        # Remove hash tag symbols
        text = text.replace('#', '')
        # Lowercase the text
        text = text.lower()
        # result
        return text

    def _process_article_text(self, text):
        # Remove paragraph tags
        text = re.sub('<p>|</p>', '', text)
        # Lowercase the text
        text = text.lower()
        # result
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

