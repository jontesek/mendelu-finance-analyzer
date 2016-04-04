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
        self.files_count = 1
        self.documents_per_file = 50000  # constant


    # MAIN PROCESSING

    def process_documents_for_company(self, doc_type, company_id, from_date, days_delay, price_type, total_file_name=False):
        # Set stock prices for given company.
        prices = self.stock_processor.set_stock_prices(company_id, from_date, price_type)
        if not prices:
            return False
        # Get documents from DB.
        if doc_type == 'fb_post':
            documents = self.db_model.get_fb_posts_for_company(company_id, from_date)
        elif doc_type == 'fb_comment':
            documents = self.db_model.get_fb_comments_for_company(company_id, from_date)
        elif doc_type == 'article':
            documents = self.db_model.get_articles_for_company(company_id, from_date)
        elif doc_type == 'tweet':
            documents = self.db_model.get_tweets_for_company(company_id, from_date)
        # Check if documents exists.
        if not documents:
            return False
        # Process documents - create a list for writing to a file.
        new_docs_list = []
        for doc in documents:
            # Get document publication date
            if doc_type == 'fb_post' or doc_type == 'fb_comment':
                doc_date = datetime.datetime.utcfromtimestamp(doc['created_timestamp']).date()
            elif doc_type == 'article':
                doc_date = doc['published_date'].date()
            elif doc_type == 'tweet':
                doc_date = doc['created_at'].date()
            # Get stock price movement direction
            movement_direction = self.stock_processor.get_price_movement_with_delay(doc_date, days_delay)
            # If the company was not on the stock exchange on this date, skip the post.
            if not movement_direction:
                continue
            # Skip constant direction
            if movement_direction == 'const':
                continue
            # Edit document text
            if doc_type == 'fb_post' or doc_type == 'fb_comment' or doc_type == 'tweet':
                doc_text = self._process_facebook_text(doc['text'])
            elif doc_type == 'article':
                doc_text = self._process_article_text(doc['text'])
            # Add created data to the list.
            new_docs_list.append([movement_direction, doc_text])
            # Increment current file's documents count
            self.documents_count += 1
        # Choose the correct file name (bulk vs individual generating).
        if total_file_name:
            file_name = total_file_name
            file_mode = 'a'
        else:
            file_name = doc_type+'_%s_%s_%s_%d' % (company_id, price_type, from_date.strftime('%Y-%m-%d'), days_delay)
            file_mode = 'w'
        # Write data to the file
        self.text_writer.write_file_for_vectorization(file_name, new_docs_list, file_mode)

    def process_documents_for_all_companies(self, doc_type, from_date, days_delay, price_type):
        # Reset documents count (for given doc_type)
        self.documents_count = 0
        self.files_count = 0
        # Create file name
        file_name = doc_type+'_all_%s_%s_%s-0' % (price_type, from_date.strftime('%Y-%m-%d'), str(days_delay))
        # Process all companies
        for comp in self.db_model.get_companies():
            print('===Company %d===') % comp[0]
            # Check if the file should be ended.
            if self.documents_count > self.documents_per_file:
                print('>>>NEW FILE')
                self.files_count += 1
                self.documents_count = 0
                file_name = re.sub('\d+$', str(self.files_count), file_name)
            # Process and write data for one company.
            self.process_documents_for_company(doc_type, comp[0], from_date, days_delay, price_type, file_name)

    # TEXT processing

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

