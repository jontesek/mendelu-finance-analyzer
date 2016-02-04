import datetime
import re

from ExportsDbModel import ExportsDbModel
from FaCommon.TextWriter import TextWriter


class Exports(object):

    def __init__(self, out_dir):
        self.db_model = ExportsDbModel()
        self.text_writer = TextWriter(out_dir)
        self.pattern_http = re.compile('https?:\/\/.* ')

    def export_documents_for_company(self, doc_type, company_id, from_date):
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
            # Edit document text
            if doc_type == 'fb_post' or doc_type == 'fb_comment' or doc_type == 'tweet':
                doc_text = self._process_facebook_text(doc['text'])
            elif doc_type == 'article':
                doc_text = self._process_article_text(doc['text'])
            # Skip empty text
            if len(doc_text) == 0:
                continue
            # Add created data to the list.
            new_docs_list.append([doc_date.strftime('%d.%m.%Y'), doc_text])

        # Choose the correct file name.
        file_name = doc_type+'_%s' % company_id
        # Write data to the file
        self.text_writer.write_file_for_vectorization(file_name, new_docs_list, 'w')


    def export_prices(self, company_id, from_date):
        prices = self.db_model.get_stock_prices(company_id, from_date)
        file_name = 'prices_%s' % company_id
        self.text_writer.write_file_for_vectorization(file_name, prices, 'w')


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