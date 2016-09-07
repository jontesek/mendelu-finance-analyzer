import os

from LexiconSentimentAnalyzer import LexiconSentimentAnalyzer
from BasicDbModel import BasicDbModel
from FaCommon.TextWriter import TextWriter
from FaCommon.TextProcessing import TextProcessing


class SimpleExporter(object):

    def __init__(self, output_dir, verbose=False):
        self.dbmodel = BasicDbModel()
        self.s_analyzer = LexiconSentimentAnalyzer()
        self.text_writer = TextWriter(os.path.abspath(output_dir))
        self.verbose = verbose

    def analyze_company(self, company_id, from_date, to_date):
        """
        Analyze documents of the given company - just write VADER scores of every document.
        :param company_id:
        :param from_date:
        :param to_date:
        :return:
        """
        print('==Company %d==') % company_id
        # For every source, create a standalone file.
        for source in ['articles', 'fb_posts', 'fb_comments', 'tweets']:
            self._analyze_documents_by_source(company_id, source, from_date, to_date)
        # end

    def analyze_all_companies(self, from_date, to_date):
        companies = self.dbmodel.get_companies()
        # For every source, create a standalone file.
        for source in ['articles', 'fb_posts', 'fb_comments', 'tweets']:
            print('====Processing %s====') % source
            # Prepare file.
            header_line = ['company_id', 'date', 'sentiment_number', 'sentiment_polarity']
            self.text_writer.write_file([header_line], source, 'csv', ',', 'w')
            # Browse all companies.
            for comp in companies:
                print('==Company %d==') % comp['id']
                self._analyze_company_source(comp['id'], source, from_date, to_date, source)
                #break


    def _analyze_company_source(self, company_id, source_type, from_date, to_date, write_to_filename):
        # Get documents.
        documents = getattr(self.dbmodel, 'get_'+source_type)(company_id, from_date, to_date)
        # Create a final list.
        docs_list = []
        for doc in documents:
            #print doc['id'],
            # Process text.
            if source_type == 'articles':
                text = TextProcessing.process_article_text(doc['text'])
            else:
                text = TextProcessing.process_facebook_text(doc['text'])
            # Skip empty documents.
            if len(text) == 0:
                continue
            # Get sentiment values of the text.
            if source_type == 'articles':
                sentiment_number = self.s_analyzer.calculate_vader_sentiment('custom_dict_orig', text, True)
            else:
                sentiment_number = self.s_analyzer.calculate_vader_sentiment('custom_dict_orig', text, False)
            sentiment_polarity = self.s_analyzer.format_sentiment_value(sentiment_number)
            # Save data.
            doc_date = self._get_doc_date(source_type, doc)
            docs_list.append([company_id, doc_date, sentiment_number, sentiment_polarity])
        # Write to file.
        self.text_writer.write_file(docs_list, write_to_filename, 'csv', ',', 'a')


    def _analyze_documents_by_source(self, company_id, source_type, from_date, to_date, write_to_filename=False):
        # Get documents
        documents = getattr(self.dbmodel, 'get_'+source_type)(company_id, from_date, to_date)
        # Create a final list
        docs_list = []
        for doc in documents:
            # Process text
            if source_type == 'articles':
                text = TextProcessing.process_article_text(doc['text'])
            else:
                text = TextProcessing.process_facebook_text(doc['text'])
            # Skip empty documents
            if len(text) == 0:
                continue
            # Get sentiment values of the text
            sent_sum, sent_division = self.s_analyzer.calculate_vader_sentiment_values('vader', text)
            # Add this to list
            docs_list.append([sent_sum, sent_division, text])
        # Prepare header
        header = ['sentiment_sum', 'sentiment_division', 'text']
        docs_list.insert(0, header)
        file_name = '%d_%s' % (company_id, source_type)
        self.text_writer.write_file(docs_list, file_name, 'csv', '\t', 'w')


    def _get_doc_date(self, source_type, doc):
        if source_type == 'articles':
            date_obj = doc['published_date']
        elif source_type in ['fb_posts', 'fb_comments']:
            date_obj = self.dbmodel.from_timestamp_to_date(doc['created_timestamp'])
        elif source_type == 'tweets':
            date_obj = doc['created_at']
        return date_obj.strftime('%Y-%m-%d')

