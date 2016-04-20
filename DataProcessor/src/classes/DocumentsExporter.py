import os
import datetime
import re

from StockPriceProcessor import StockPriceProcessor
from DocumentsExporterDbModel import DocumentsExporterDbModel
from TextWriter import TextWriter


class DocumentsExporter(object):
    """
    Export documents for conversion to vectors and classification by machine learning algorithms.
    """

    def __init__(self, file_paths):
        # DB model
        self.db_model = DocumentsExporterDbModel()
        # Path to output directory.
        self.file_paths = file_paths
        # Object for stock movements.
        self.stock_processor = StockPriceProcessor()
        # Define output document classes.
        self.doc_classes = {'up': '1', 'down': '2'}
        # Object for writing text files.
        self.text_writer = TextWriter(file_paths['output_dir'])

    # PUBLIC METHODS

    def process_documents_for_all_companies(self, doc_type, from_date, days_delay, price_type, const_boundaries,
                                            balance_classes_for_company, docs_per_file=50000, only_one_file=True):
        print('===Processing %s===') % doc_type
        # Reset document counts.
        documents_count = 0
        files_count = 0
        # Create file name.
        f_number = '' if only_one_file else '_0'
        file_name = doc_type.replace('_', '-') + '_all_%s_%s_%s%s' % \
                                                 (price_type, str(days_delay), const_boundaries[1], f_number)
        # Process all companies.
        for comp in self.db_model.get_companies():
            #print('===Company %d===') % comp[0]
            # Process and write data for one company.
            new_docs_count = self.process_documents_for_company(doc_type, comp[0], from_date, days_delay,
                                                                price_type, const_boundaries,
                                                                balance_classes_for_company, file_name)
            documents_count += new_docs_count
            # Check if the file should be ended.
            if documents_count > docs_per_file:
                print('>>>NEW FILE')
                if only_one_file:
                    break
                else:
                    files_count += 1
                    documents_count = 0
                    file_name = re.sub('\d+$', str(files_count), file_name)
        # The end.
        print('>>>All %s for all companies exported. Total docs: %d ') % \
             (doc_type, files_count * docs_per_file + documents_count)


    def process_random_documents(self, doc_type, from_date, days_delay, price_type,
                                 const_boundaries, docs_per_day):
        # Create file name.
        file_name = doc_type + '_random_%s_%s_%s' % (price_type, str(days_delay), str(const_boundaries))
        # For every day, choose random documents (from all companies).
        processed_date = from_date
        plus_day = datetime.timedelta(days=1)
        while processed_date <= datetime.datetime.now():
            print('===%s===') % str(processed_date)
            # Get documents from DB.
            if doc_type == 'fb_post':
                documents = self.db_model.get_random_fb_posts(processed_date, docs_per_day)
            elif doc_type == 'fb_comment':
                documents = self.db_model.get_random_fb_comments(processed_date, docs_per_day)
            elif doc_type == 'article':
                documents = self.db_model.get_random_articles(processed_date, docs_per_day)
            elif doc_type == 'tweet':
                documents = self.db_model.get_random_tweets(processed_date, docs_per_day)
            # Process documents.
            self._process_given_documents(documents, doc_type, days_delay, price_type, const_boundaries)
            d_list, min_class_count = self._process_given_documents(documents, doc_type, days_delay, price_type, const_boundaries)
            self._write_docs_to_file(d_list, min_class_count, doc_type, 'all', days_delay, price_type, const_boundaries, file_name)
            # Increment date.
            processed_date += plus_day
        # the end
        print('>>>Random documents for all dates exported.')


    def process_documents_for_company(self, doc_type, company_id, from_date, days_delay, price_type,
                                      const_boundaries, balance_classes, total_file_name=False):
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
        # Process the documents.
        d_list = self._process_given_documents(documents, doc_type, days_delay, price_type, const_boundaries, balance_classes)
        file_name = self._write_docs_to_file(d_list, doc_type,
                                             company_id, days_delay, price_type, const_boundaries, total_file_name)
        if not total_file_name:
            return os.path.abspath(self.file_paths['output_dir'] + '/' + file_name + '.text')
        else:
            return len(d_list)


    def change_output_dir(self, new_dir):
        self.file_paths['output_dir'] = new_dir


    # PRIVATE METHODS

    def _process_given_documents(self, documents, doc_type, days_delay, price_type, const_boundaries, balance_classes):
        # Prepare counts for class balance.
        count_class_up = 0
        count_class_down = 0
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
            # Get stock price movement direction.
            movement_direction = self.stock_processor.get_price_movement_with_delay(doc_date, days_delay, const_boundaries)
            # If the company was not on the stock exchange on this date, skip the post.
            if not movement_direction:
                continue
            # Skip documents with constant direction.
            if movement_direction == 'const':
                continue
            # Edit document text.
            if doc_type == 'fb_post' or doc_type == 'fb_comment' or doc_type == 'tweet':
                doc_text = self._process_facebook_text(doc['text'])
            elif doc_type == 'article':
                doc_text = self._process_article_text(doc['text'])
            # Add created data to the list.
            new_docs_list.append([self.doc_classes[movement_direction], doc_text])
            # Increment variables.
            if movement_direction == 'up':
                count_class_up += 1
            elif movement_direction == 'down':
                count_class_down += 1
        # If set, balance document classes.
        if balance_classes:
            min_class_count = min([count_class_up, count_class_down])
            return self._balance_documents(new_docs_list, min_class_count)
        else:
            return new_docs_list


    def _balance_documents(self, docs_list, min_class_count):
        """
        Create a new documents list, where each class will have the same number of documents.

        :param docs_list: list: (class, text).
        :param min_class_count: int: Provided minimal class count.
        :return: list
        """
        # Class counts variables.
        c_1 = 0
        c_2 = 0
        new_docs_list = []
        # Loop through all documents.
        for i, doc in enumerate(docs_list):
            if doc[0] == '1':
                c_1 += 1
                if c_1 <= min_class_count:
                    new_docs_list.append(doc)
            if doc[0] == '2':
                c_2 += 1
                if c_2 <= min_class_count:
                    new_docs_list.append(doc)
        # Edit documents
        return new_docs_list


    def _write_docs_to_file(self, docs_list, doc_type, company_id, days_delay, price_type,
                            const_boundaries, total_file_name=False):
        # Choose the correct file name (bulk vs individual generating).
        if total_file_name:
            file_name = total_file_name
            file_mode = 'a'
        else:
            file_name = doc_type.replace('_', '-') + '_%s_%s_%s_%s' % (company_id, price_type, days_delay, const_boundaries[1])
            file_mode = 'w'
        # Write data to the file.
        self.text_writer.write_file_for_vectorization(file_name, docs_list, file_mode)
        return file_name



    # TEXT processing

    def _process_facebook_text(self, text):
        # Remove whitespace.
        text = ' '.join(text.strip().split())
        # Remove hash tag symbols
        text = text.replace('#', '')
        # Remove at symbols.
        text = text.replace('@', '')
        # Lowercase the text
        text = text.lower()
        # result
        return text

    def _process_article_text(self, text):
        # Remove outer spaces.
        text = text.strip()
        # Remove paragraph tags.
        text = re.sub('<p>|</p>', '', text)
        # Lowercase the text.
        text = text.lower()
        # Result
        return text


