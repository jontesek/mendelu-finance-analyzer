import datetime
import math

from LexiconSentimentAnalyzer import LexiconSentimentAnalyzer
from SourceMetricsCalculator import SourceMetricsCalculator
from SourceMetricsCalculator2classes import SourceMetricsCalculator2classes
from TotalMetricsCalculator import TotalMetricsCalculator
from BasicDbModel import BasicDbModel
from FaCommon.TextWriter import TextWriter
from FaCommon.TextProcessing import TextProcessing
from DataProcessor.src.classes.StockPriceProcessor import StockPriceProcessor
import FaCommon.Helpers


class DocumentsAnalyzer(object):

    def __init__(self, output_dir, verbose=False):
        """
        :param output_dir: Absolute filepath to output directory.
        :param verbose: boolean: Write info to console.
        :return:
        """
        self.dbmodel = BasicDbModel()
        self.s_analyzer = LexiconSentimentAnalyzer()
        self.text_writer = TextWriter(output_dir)   # writing CSV files
        self.verbose = verbose  # verbose output
        self.stock_processor = StockPriceProcessor()    # Object for price movements
        self.source_metrics_calculator = SourceMetricsCalculator(output_dir)
        self.total_metrics_calculator = TotalMetricsCalculator(output_dir)
        self.source_metrics_calculator_2_classes = SourceMetricsCalculator2classes(output_dir)

    ## Analyze output file

    def analyze_all_companies(self, from_date, to_date, file_name, price_type, const_boundaries, used_dict_name='vader', classes_count=3):
        """
        Analyze all documents for all companies.

        :param from_date:
        :param to_date:
        :param file_name:
        :param price_type:
        :param used_dict_name:
        :return:
        """
        # Reset files.
        self.text_writer.write_econometric_file(file_name, [self._get_days_stats_header()], 'w')
        total_m_header = self.total_metrics_calculator.get_total_metrics_header()
        self.text_writer.write_econometric_file(file_name + '_total-metrics', [total_m_header], 'w')
        source_m_header = self.source_metrics_calculator.get_source_metrics_header()
        self.text_writer.write_econometric_file(file_name + '_source-metrics', [source_m_header], 'w')
        # Process companies
        companies = self.dbmodel.get_companies_order_by_total_documents(from_date, to_date)
        for comp in companies:
            print("<<<<<Company %d>>>>>") % comp['id']
            if not self.verbose:
                with FaCommon.Helpers.suppress_stdout():
                    self.analyze_company(comp['id'], from_date, to_date, file_name, price_type, const_boundaries, used_dict_name, False, classes_count)
            else:
                self.analyze_company(comp['id'], from_date, to_date, file_name, price_type, const_boundaries, used_dict_name, False, classes_count)
        print('>>>All stuff saved.')

    def analyze_company(self, company_id, from_date, to_date, file_name, price_type, const_boundaries, used_dict_name, write_header=False, classes_count=3):
        """
        Analyze documents about company (from_date -> present date).

        :return: list of days, where every row contains information for documents for this day.
        """
        # Prepare variables.
        examined_date = from_date
        last_date = to_date
        total_data = []
        max_sent = float('-inf')

        # Set stock prices for this company ID.
        self.stock_processor.set_stock_prices(company_id, examined_date, price_type)
        #exit(self.stock_processor.get_price_movement_with_delay(examined_date, 2))

        # Prepare list for writing to a file.
        # For every day (from "from_date" to "to_date"), query the DB for documents created on the day.
        while examined_date <= last_date:
            print("===%s===") % examined_date
            # For every document type, process all documents and count number of neutral, positive, negative documents.
            yahoo_values = self._process_yahoo(company_id, examined_date, used_dict_name)
            fb_p_values = self._process_fb_posts(company_id, examined_date, used_dict_name)
            fb_c_values = self._process_fb_comments(company_id, examined_date, used_dict_name)
            tw_values = self._process_tweets(company_id, examined_date, used_dict_name)
            # Save acquired data
            day_data = [
                company_id,
                examined_date.strftime('%d.%m.%Y'),
                fb_p_values['neu'], fb_p_values['pos'], fb_p_values['neg'],
                fb_c_values['neu'], fb_c_values['pos'], fb_c_values['neg'],
                yahoo_values['neu'], yahoo_values['pos'], yahoo_values['neg'],
                tw_values['neu'], tw_values['pos'], tw_values['neg'],
            ]
            # Get stock price movement direction for 1,2,3 days from examined date. Also for previous day.
            day_data.append(self.stock_processor.get_price_movement_with_delay(examined_date, -1, const_boundaries))
            day_data.append(self.stock_processor.get_price_movement_with_delay(examined_date, 1, const_boundaries))
            day_data.append(self.stock_processor.get_price_movement_with_delay(examined_date, 2, const_boundaries))
            day_data.append(self.stock_processor.get_price_movement_with_delay(examined_date, 3, const_boundaries))
            # Calculate simple sentiment for all sources.
            fb_post_s = self._calc_source_sentiment(fb_p_values)
            fb_comment_s = self._calc_source_sentiment(fb_c_values)
            yahoo_s = self._calc_source_sentiment(yahoo_values)
            twitter_s = self._calc_source_sentiment(tw_values)
            day_data.extend([fb_post_s, fb_comment_s, yahoo_s, twitter_s])
            # Calculate overall sentiment for the day.
            (max_sent, day_sent) = self._calc_overall_sentiment_for_day(max_sent, fb_p_values, fb_c_values, yahoo_values, tw_values)
            day_data.append(day_sent)
            # Save day data to total data.
            total_data.append(day_data)
            # Increment examined date.
            examined_date = examined_date + datetime.timedelta(days=1)

        # Normalize sentiment values.
        for i, day_data in enumerate(total_data):
            norm_sent = self._normalize_sentiment(total_data[i][-1], max_sent)
            string_sent = self._format_sentiment(norm_sent)
            total_data[i][-1] = string_sent

        # Write results to file.
        if write_header:
            total_data.insert(0, self._get_days_stats_header())
            self.text_writer.write_econometric_file(file_name, total_data, 'w')
            del(total_data[0])
        else:
            self.text_writer.write_econometric_file(file_name, total_data, 'a')

        # Calculate metrics by source.
        m_filename = file_name + '_source-metrics'
        if classes_count == 3:
            self.source_metrics_calculator.calculate_metrics_by_source(company_id, total_data, m_filename, price_type, write_header)
        else:
            self.source_metrics_calculator_2_classes.calculate_metrics_by_source(company_id, total_data, m_filename, price_type, write_header)

        # Calculate total metrics.
        m_filename = file_name + '_total-metrics'
        self.total_metrics_calculator.calculate_total_metrics(company_id, total_data, m_filename, price_type, write_header)



    #### PRIVATE methods for processing documents

    def _process_fb_posts(self, company_id, examined_date, used_dict_name='vader'):
        # Select all FB posts for given company created on given date.
        posts = self.dbmodel.get_daily_fb_posts(company_id, examined_date)
        counter = {'pos': 0, 'neu': 0, 'neg': 0}
        # Calculate sentiment for all posts
        for post in posts:
            #print("FB post: %s") % post['id'],
            post_text = TextProcessing.process_facebook_text(post['text'])
            if len(post_text) == 0:
                continue    # skip empty posts
            sent_value = self.s_analyzer.calculate_vader_sentiment(used_dict_name, post_text, False)
            polarity = self.s_analyzer.format_sentiment_value(sent_value)
            counter[polarity] += 1
            #print("| %s ... %s") % (str(round(sent_value, 4)), polarity)
        # result
        return counter

    def _process_fb_comments(self, company_id, examined_date, used_dict_name='vader'):
        # Select all FB comments.
        comments = self.dbmodel.get_daily_fb_comments(company_id, examined_date)
        counter = {'pos': 0, 'neu': 0, 'neg': 0}
        # Calculate sentiment for all posts
        for com in comments:
            #print("FB comment: %s") % com['id'],
            com_text = TextProcessing.process_facebook_text(com['text'])
            if len(com_text) == 0:
                continue    # skip empty comments
            sent_value = self.s_analyzer.calculate_vader_sentiment(used_dict_name, com_text, False)
            polarity = self.s_analyzer.format_sentiment_value(sent_value)
            counter[polarity] += 1
            #print("| %s ... %s") % (str(round(sent_value, 4)), polarity)
        # result
        return counter

    def _process_yahoo(self, company_id, examined_date, used_dict_name='vader'):
        # Select all Yahoo Finance articles.
        articles = self.dbmodel.get_daily_articles(company_id, examined_date)
        counter = {'pos': 0, 'neu': 0, 'neg': 0}
        # Calculate sentiment for all articles
        for art in articles:
            #print("Yahoo article: %s") % art['id'],
            art_text = TextProcessing.process_article_text(art['text'])
            if len(art_text) == 0:
                continue    # skip empty articles
            sent_value = self.s_analyzer.calculate_vader_sentiment(used_dict_name, art_text, True)
            polarity = self.s_analyzer.format_sentiment_value(sent_value)
            counter[polarity] += 1
            #print("| %s ... %s") % (str(round(sent_value, 4)), polarity)
        # result
        return counter

    def _process_tweets(self, company_id, examined_date, used_dict_name='vader'):
        # Select all Yahoo Finance articles.
        tweets = self.dbmodel.get_daily_tweets(company_id, examined_date)
        counter = {'pos': 0, 'neu': 0, 'neg': 0}
        # Calculate sentiment for all articles.
        for tw in tweets:
            #print("Tweet: %s") % tw['tw_id'],
            tw_text = TextProcessing.process_facebook_text(tw['text'])
            if len(tw_text) == 0:
                continue    # skip empty tweets
            sent_value = self.s_analyzer.calculate_vader_sentiment(used_dict_name, tw_text, False)
            polarity = self.s_analyzer.format_sentiment_value(sent_value)
            counter[polarity] += 1
            #print("| %s ... %s") % (str(round(sent_value, 4)), polarity)
        # result
        return counter

    ## PRIVATE methods for determining sentiment of the whole day

    def _calc_source_sentiment(self, s_dict):
        """
        Calculate sentiment for given source dictionary.

        :param s_dict: dictionary (sentiment -> number of documents}
        :return: string (pos, neg, neu)
        """
        max_s = max(s_dict.keys(), key=lambda k: s_dict[k])
        # If neutral value is also the biggest one, choose it.
        if s_dict['neu'] == s_dict[max_s]:
            return 'neu'
        return max_s


    @staticmethod
    def _calc_overall_sentiment_for_day(max_sent, fb_p_values, fb_c_values, yahoo_values, tw_values):
        # Calculate numeric sentiment
        fb_p_sent = fb_p_values['pos'] - fb_p_values['neg']
        fb_c_sent = fb_c_values['pos'] - fb_p_values['neg']
        yahoo_sent = yahoo_values['pos'] - fb_p_values['neg']
        tw_sent = tw_values['pos'] - fb_p_values['neg']
        overall_sent = fb_p_sent + fb_c_sent + yahoo_sent + tw_sent
        #print fb_p_sent,fb_c_sent,yahoo_sent,tw_sent
        # Is the new sentiment larger than current largest one?
        if overall_sent > max_sent:
            max_sent = overall_sent
        return max_sent, overall_sent

    @staticmethod
    def _normalize_sentiment(score, alpha=100):
        """
        Normalize the score to be between -1 and 1 using an alpha that approximates the max expected value.
        """
        try:
            norm_score = score/math.sqrt((score*score) + alpha)
        except ZeroDivisionError:
            norm_score = score
        return norm_score

    @staticmethod
    def _format_sentiment(norm_score):
        if -0.1 < norm_score < 0.1:
            return 'neu'
        elif norm_score > 0:
            return 'pos'
        elif norm_score < 0:
            return 'neg'

    @staticmethod
    def _get_days_stats_header():
        header_days = [
            'company_id', 'date',
            'fb_post_neutral', 'fb_post_positive', 'fb_post_negative',
            'fb_comment_neutral', 'fb_comment_positive', 'fb_comment_negative',
            'yahoo_neutral', 'yahoo_positive', 'yahoo_negative',
            'twitter_neutral', 'twitter_positive', 'twitter_negative',
            'stock_dir_-1', 'stock_dir_1', 'stock_dir_2', 'stock_dir_3',
            'sentiment_fb_post', 'sentiment_fb_comment', 'sentiment_yahoo', 'sentiment_twitter',
            'overall_sentiment',
        ]
        return header_days
