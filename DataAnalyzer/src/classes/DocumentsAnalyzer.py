import datetime
import os

from LexiconSentimentAnalyzer import LexiconSentimentAnalyzer
from BasicDbModel import BasicDbModel
from FaCommon.TextWriter import TextWriter
from FaCommon.TextProcessing import TextProcessing


class DocumentsAnalyzer(object):

    def __init__(self, output_dir):
        self.dbmodel = BasicDbModel()
        self.s_analyzer = LexiconSentimentAnalyzer()
        self.text_writer = TextWriter(os.path.abspath(output_dir))

    ## PUBLIC methods

    def analyze_all_companies(self, from_date, to_date, file_name):
        companies = self.dbmodel.get_companies()
        for comp in companies:
            print("<<<<<Company %d>>>>>") % comp['id']
            self.analyze_company(comp['id'], from_date, to_date, file_name)
        print('>>>All stuff saved.')

    def analyze_company(self, company_id, from_date, to_date, file_name):
        """
        Analyze documents about company (from_date -> present date).
        :param company_id: int
        :param from_date: string
        :return: list of days, where every row contains information for documents for this day.
        """
        # Prepare variables
        examined_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        last_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
        total_data = []
        # Prepare list for writing to a file.
        # For every day (from "from_date" to present date), query the DB for documents created on the day.
        while examined_date <= last_date:
            print("===%s===") % examined_date.date()
            # For every document type, process all documents and count number of neutral, positive, negative documents.
            fb_p_values = self._process_fb_posts(company_id, examined_date)
            fb_c_values = self._process_fb_comments(company_id, examined_date)
            yahoo_values = self._process_yahoo(company_id, examined_date)
            tw_values = self._process_tweets(company_id, examined_date)
            # Save acquired data
            day_data = [
                company_id,
                examined_date.strftime('%d.%m.%Y'),
                fb_p_values['neu'], fb_p_values['pos'], fb_p_values['neg'],
                fb_c_values['neu'], fb_c_values['pos'], fb_c_values['neg'],
                yahoo_values['neu'], yahoo_values['pos'], yahoo_values['neg'],
                tw_values['neu'], tw_values['pos'], tw_values['neg'],
            ]
            total_data.append(day_data)
            print day_data
            # Increment examined date
            examined_date = examined_date + datetime.timedelta(days=1)
        # Write result to file
        self.text_writer.write_econometric_file(file_name, total_data, 'a')


    ## PRIVATE methods

    def _process_fb_posts(self, company_id, examined_date):
        # Select all FB posts for given company created on given date.
        posts = self.dbmodel.get_daily_fb_posts(company_id, examined_date)
        counter = {'pos': 0, 'neu': 0, 'neg': 0}
        # Calculate sentiment for all posts
        for post in posts:
            print("FB post: %s") % post['id'],
            post_text = TextProcessing.process_facebook_text(post['text'])
            if len(post_text) == 0:
                continue    # skip empty posts
            sent_value = self.s_analyzer.calculate_vader_sentiment('vader', post_text)
            polarity = self.s_analyzer.format_sentiment_value(sent_value)
            counter[polarity] += 1
            print("| %s ... %s") % (str(round(sent_value, 4)), polarity)
        # result
        return counter

    def _process_fb_comments(self, company_id, examined_date):
        # Select all FB comments.
        comments = self.dbmodel.get_daily_fb_comments(company_id, examined_date)
        counter = {'pos': 0, 'neu': 0, 'neg': 0}
        # Calculate sentiment for all posts
        for com in comments:
            print("FB comment: %s") % com['id'],
            com_text = TextProcessing.process_facebook_text(com['text'])
            if len(com_text) == 0:
                continue    # skip empty comments
            sent_value = self.s_analyzer.calculate_vader_sentiment('vader', com_text)
            polarity = self.s_analyzer.format_sentiment_value(sent_value)
            counter[polarity] += 1
            print("| %s ... %s") % (str(round(sent_value, 4)), polarity)
        # result
        return counter

    def _process_yahoo(self, company_id, examined_date):
        # Select all Yahoo Finance articles.
        articles = self.dbmodel.get_daily_articles(company_id, examined_date)
        counter = {'pos': 0, 'neu': 0, 'neg': 0}
        # Calculate sentiment for all articles
        for art in articles:
            print("Yahoo article: %s") % art['id'],
            art_text = TextProcessing.process_article_text(art['text'])
            if len(art_text) == 0:
                continue    # skip empty articles
            sent_value = self.s_analyzer.calculate_vader_sentiment('vader', art_text)
            polarity = self.s_analyzer.format_sentiment_value(sent_value)
            counter[polarity] += 1
            print("| %s ... %s") % (str(round(sent_value, 4)), polarity)
        # result
        return counter

    def _process_tweets(self, company_id, examined_date):
        # Select all Yahoo Finance articles.
        tweets = self.dbmodel.get_daily_tweets(company_id, examined_date)
        counter = {'pos': 0, 'neu': 0, 'neg': 0}
        # Calculate sentiment for all articles
        for tw in tweets:
            print("Tweet: %s") % tw['tw_id'],
            tw_text = TextProcessing.process_facebook_text(tw['text'])
            if len(tw_text) == 0:
                continue    # skip empty tweets
            sent_value = self.s_analyzer.calculate_vader_sentiment('vader', tw_text)
            polarity = self.s_analyzer.format_sentiment_value(sent_value)
            counter[polarity] += 1
            print("| %s ... %s") % (str(round(sent_value, 4)), polarity)
        # result
        return counter
