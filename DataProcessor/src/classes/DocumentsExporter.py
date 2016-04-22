import os
import datetime
import re
import pytz

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


    def process_companies_by_source(self, file_desc, doc_type, from_date, to_date, days_delay, price_type,
                                    const_boundaries, balance_classes_for_company, docs_per_file=100000):
        # Get company IDs.
        company_ids = self.db_model.get_companies_by_doc_type(doc_type)
        c_ids_list = [x[0] for x in company_ids]
        # Process all selected companies.
        self.process_documents_for_selected_companies(
            c_ids_list, doc_type, from_date, to_date, days_delay, price_type,
            const_boundaries, balance_classes_for_company, docs_per_file, file_desc)


    def process_documents_for_selected_companies(self, companies_ids, doc_type, from_date, to_date, days_delay,
                                                 price_type, const_boundaries, balance_classes_for_company,
                                                 docs_per_file=100000, companies_filename=False):
        print('===Processing %s===') % doc_type
        # Reset document counts.
        documents_count = 0
        # Calculate number of documents per company.
        docs_per_company = int(round(docs_per_file / float(len(companies_ids))))
        # Choose file description string.
        if companies_filename:
            fs_comp = companies_filename
        else:
            if len(companies_ids) < 5:
                fs_comp = '-'.join(str(v) for v in companies_ids)
            else:
                fs_comp = 'm%s' % len(companies_ids)
        # Create file name.
        file_name = '%s_%s_%s_%s_%s' % \
                    (doc_type.replace('_', '-'), fs_comp, price_type, str(days_delay), const_boundaries[1])

        # Process all companies.
        for comp in self.db_model.get_selected_companies(companies_ids):
            print('===Company %d===') % comp[0]
            # Process and write data for one company.
            new_docs_count = self.process_daily_documents_for_company(
                doc_type, comp[0], from_date, to_date, days_delay, price_type, const_boundaries,
                balance_classes_for_company, docs_per_company, file_name)
            print new_docs_count
            # Increment docs count.
            documents_count += new_docs_count
            # Check if the file should be ended.
            if documents_count > docs_per_file:
                print('>>>END FILE')
        # The end.
        print('>>>All %s for selected companies exported. Total docs: %d ') % (doc_type, documents_count)


    def process_daily_documents_for_company(self, doc_type, company_id, from_date, to_date, days_delay, price_type,
                                            const_boundaries, balance_classes, max_docs_per_company, total_file_name=False):
        # Set stock prices for given company.
        prices = self.stock_processor.set_stock_prices(company_id, from_date, price_type)
        if not prices:
            return False
        # Calculate number of documents per day: n = docs_per_company / days(to_date - from_date)
        date_delta = to_date - from_date
        docs_per_day = int(round(max_docs_per_company / float(date_delta.days)))
        docs_per_day *= 2   # To get more documents, increase the count.
        #docs_per_day = 200  # For Twitter and 4 companies.
        docs_per_day = 10   # For Facebook
        # Example: 25 000 docs per company / 241 days = 104 docs per day
        print ('>>Docs per company/days/per day: %d, %d, %d') % (max_docs_per_company, date_delta.days, docs_per_day)
        # Define variables.
        docs_query_limit = 400  # Do not change -- cached queries won't work. Original value: 400.
        total_doc_list = []
        docs_counter = 0
        processed_date = from_date
        day_plus = datetime.timedelta(days=1)
        # For every day, get documents from DB.
        while processed_date <= to_date:
            #print processed_date
            # Get documents for current date from DB.
            if doc_type == 'fb_post':
                daily_documents = self.db_model.get_daily_fb_posts_for_company(company_id, processed_date, docs_query_limit)
            elif doc_type == 'fb_comment':
                daily_documents = self.db_model.get_daily_fb_comments_for_company(company_id, processed_date, docs_query_limit)
            elif doc_type == 'article':
                daily_documents = self.db_model.get_daily_articles_for_company(company_id, processed_date, docs_query_limit)
            elif doc_type == 'tweet':
                daily_documents = self.db_model.get_daily_tweets_for_company(company_id, processed_date, docs_query_limit)
            else:
                raise ValueError('Unknown document type.')
            # Process the documents.
            d_list = self._process_given_documents(daily_documents, doc_type, days_delay, price_type, const_boundaries, False)
            #print('Processed docs: %d') % d_length
            # Increment day.
            processed_date += day_plus
            # If there are no documents, continue with next date.
            if not d_list:
                continue
            # Check and edit number of available documents.
            if len(d_list) > docs_per_day:
                d_list = d_list[0:docs_per_day]
            #print('Saved docs: %d') % len(d_list)
            # Add documents to total list.
            total_doc_list.extend(d_list)
            docs_counter += len(d_list)
            # Check number of already saved documents.
            if docs_counter > max_docs_per_company:
                print('Max documents count (%d) for company reached.') % max_docs_per_company
                break   # Stop and write documents to file.

        # Check if there are any documents.
        if not total_doc_list:
            return False
        # Write documents from all dates.
        self._write_docs_to_file(total_doc_list, doc_type, company_id, days_delay, price_type, const_boundaries, total_file_name)
        # Return some information.
        return len(total_doc_list)


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
        else:
            raise ValueError('Unknown document type.')
        # Process the documents.
        d_list = self._process_given_documents(documents, doc_type, days_delay, price_type, const_boundaries, balance_classes)
        # Check if there are were any documents.
        if not d_list:
            return False
        # Write documents to correct file.
        self._write_docs_to_file(d_list, doc_type, company_id, days_delay, price_type, const_boundaries, total_file_name)
        # Return some information.
        return len(d_list)


    def change_output_dir(self, new_dir):
        # Update object attributes.
        self.file_paths['output_dir'] = new_dir
        self.text_writer.output_dir = new_dir
        # Check if directory exists. If it doesn't, create it.
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)


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
            else:
                raise ValueError('Unknown document type.')
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
            # Check if the document is not empty.
            if not doc_text:
                continue
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
        # Remove hash tag symbols.
        text = text.replace('#', '')
        # Remove at symbols.
        text = text.replace('@', '')
        # Remove URL links.
        text = re.sub(r'https?://\S+', 'XURL', text)
        # Lowercase the text.
        text = text.lower()
        # result
        return text

    def _process_article_text(self, text):
        # Remove URL links.
        #text = re.sub(r'(https?://\S+)|(www\.\w+\.\S+)', 'URL', text)
        text = re.sub(r'https?://\S+', 'XURL', text)
        # Remove paragraph tags.
        text = re.sub(r'<p>|</p>', '', text)
        # Lowercase the text.
        text = text.lower()
        # Result
        return text
