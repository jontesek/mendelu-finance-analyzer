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
        print('====Company %d====') % company_id
        # For every source, create a standalone file.
        for source in ['articles', 'fb_posts', 'fb_comments', 'tweets']:
            self._analyze_documents_by_source(company_id, source, from_date, to_date)
        # end

    def _analyze_documents_by_source(self, company_id, source_type, from_date, to_date):
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
        # Write list to file
        file_name = '%d_%s' % (company_id, source_type)
        self.text_writer.write_file(docs_list, file_name, 'csv', '\t', 'w')

