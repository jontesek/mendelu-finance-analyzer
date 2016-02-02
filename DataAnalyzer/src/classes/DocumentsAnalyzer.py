import datetime
import os
import math

from LexiconSentimentAnalyzer import LexiconSentimentAnalyzer
from BasicDbModel import BasicDbModel
from FaCommon.TextWriter import TextWriter
from FaCommon.TextProcessing import TextProcessing
from DataProcessor.src.classes.StockPriceProcessor import StockPriceProcessor
import FaCommon.Helpers


class DocumentsAnalyzer(object):

    def __init__(self, output_dir, verbose=False):
        self.dbmodel = BasicDbModel()
        self.s_analyzer = LexiconSentimentAnalyzer()
        self.text_writer = TextWriter(os.path.abspath(output_dir))
        self.verbose = verbose
        # Object for stock movements
        self.stock_processor = StockPriceProcessor()
        # Dict for testing results
        self.evaluated_results = {}

    ## PUBLIC methods

    def analyze_all_companies(self, from_date, to_date, file_name):
        # Prepare header
        header = [
            'company_id', 'date',
            'fb_post_neutral', 'fb_post_positive', 'fb_post_negative',
            'fb_comment_neutral', 'fb_comment_positive', 'fb_comment_negative',
            'yahoo_neutral', 'yahoo_positive', 'yahoo_negative',
            'twitter_neutral', 'twitter_positive', 'twitter_negative',
            'stock_dir_-1', 'stock_dir_1', 'stock_dir_2', 'stock_dir_3',
            'overall_sentiment'
        ]
        # Reset files
        self.text_writer.write_econometric_file(file_name, [header], 'w')
        self.text_writer.write_econometric_file('metrics', [['Metrics']], 'w')
        # Process companies
        companies = self.dbmodel.get_companies_order_by_total_documents(from_date, to_date)
        for comp in companies:
            print("<<<<<Company %d>>>>>") % comp['id']
            if not self.verbose:
                with FaCommon.Helpers.suppress_stdout():
                    self.analyze_company(comp['id'], from_date, to_date, file_name)
            else:
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
        examined_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        last_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        total_data = []
        max_sent = float('-inf')

        # Set stock prices for this company ID.
        self.stock_processor.set_stock_prices(company_id, examined_date)
        #exit(self.stock_processor.get_price_movement_with_delay(examined_date, 2))

        # Prepare list for writing to a file.
        # For every day (from "from_date" to "to_date"), query the DB for documents created on the day.
        while examined_date <= last_date:
            print("===%s===") % examined_date
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
            # Get stock price movement direction for 1,2,3 days from examined date. Also for previous day.
            day_data.append(self.stock_processor.get_price_movement_with_delay(examined_date, -1))
            day_data.append(self.stock_processor.get_price_movement_with_delay(examined_date, 1))
            day_data.append(self.stock_processor.get_price_movement_with_delay(examined_date, 2))
            day_data.append(self.stock_processor.get_price_movement_with_delay(examined_date, 3))
            # Calculate overall sentiment for the day.
            (max_sent, day_sent) = self._calc_overall_sentiment_for_day(max_sent, fb_p_values, fb_c_values, yahoo_values, tw_values)
            day_data.append(day_sent)
            # Save date to total data.
            #print(day_data)
            total_data.append(day_data)
            # Increment examined date.
            examined_date = examined_date + datetime.timedelta(days=1)

        # Normalize sentiment values.
        for i, day_data in enumerate(total_data):
            norm_sent = self._normalize_sentiment(total_data[i][-1], max_sent)
            string_sent = self._format_sentiment(norm_sent)
            total_data[i][-1] = string_sent

        # Write result to file.
        self.text_writer.write_econometric_file(file_name, total_data, 'a')

        # Evaluate results
        self.evaluated_results[company_id] = self._evaluate_results_for_company(total_data)
        metrics = self._calc_metrics_from_results(company_id)
        # Save metrics to a file.
        m_list = [['<<<<<Company %d>>>>>' % company_id]]
        m_list.extend(self._format_metrics_to_list(metrics))
        self.text_writer.write_econometric_file('metrics', m_list, 'a')


    ## PRIVATE methods

    def _process_fb_posts(self, company_id, examined_date):
        # Select all FB posts for given company created on given date.
        posts = self.dbmodel.get_daily_fb_posts(company_id, examined_date)
        counter = {'pos': 0, 'neu': 0, 'neg': 0}
        # Calculate sentiment for all posts
        for post in posts:
            #print("FB post: %s") % post['id'],
            post_text = TextProcessing.process_facebook_text(post['text'])
            if len(post_text) == 0:
                continue    # skip empty posts
            sent_value = self.s_analyzer.calculate_vader_sentiment('vader', post_text)
            polarity = self.s_analyzer.format_sentiment_value(sent_value)
            counter[polarity] += 1
            #print("| %s ... %s") % (str(round(sent_value, 4)), polarity)
        # result
        return counter

    def _process_fb_comments(self, company_id, examined_date):
        # Select all FB comments.
        comments = self.dbmodel.get_daily_fb_comments(company_id, examined_date)
        counter = {'pos': 0, 'neu': 0, 'neg': 0}
        # Calculate sentiment for all posts
        for com in comments:
            #print("FB comment: %s") % com['id'],
            com_text = TextProcessing.process_facebook_text(com['text'])
            if len(com_text) == 0:
                continue    # skip empty comments
            sent_value = self.s_analyzer.calculate_vader_sentiment('vader', com_text)
            polarity = self.s_analyzer.format_sentiment_value(sent_value)
            counter[polarity] += 1
            #print("| %s ... %s") % (str(round(sent_value, 4)), polarity)
        # result
        return counter

    def _process_yahoo(self, company_id, examined_date):
        # Select all Yahoo Finance articles.
        articles = self.dbmodel.get_daily_articles(company_id, examined_date)
        counter = {'pos': 0, 'neu': 0, 'neg': 0}
        # Calculate sentiment for all articles
        for art in articles:
            #print("Yahoo article: %s") % art['id'],
            art_text = TextProcessing.process_article_text(art['text'])
            if len(art_text) == 0:
                continue    # skip empty articles
            sent_value = self.s_analyzer.calculate_vader_sentiment('vader', art_text)
            polarity = self.s_analyzer.format_sentiment_value(sent_value)
            counter[polarity] += 1
            #print("| %s ... %s") % (str(round(sent_value, 4)), polarity)
        # result
        return counter

    def _process_tweets(self, company_id, examined_date):
        # Select all Yahoo Finance articles.
        tweets = self.dbmodel.get_daily_tweets(company_id, examined_date)
        counter = {'pos': 0, 'neu': 0, 'neg': 0}
        # Calculate sentiment for all articles.
        for tw in tweets:
            #print("Tweet: %s") % tw['tw_id'],
            tw_text = TextProcessing.process_facebook_text(tw['text'])
            if len(tw_text) == 0:
                continue    # skip empty tweets
            sent_value = self.s_analyzer.calculate_vader_sentiment('vader', tw_text)
            polarity = self.s_analyzer.format_sentiment_value(sent_value)
            counter[polarity] += 1
            #print("| %s ... %s") % (str(round(sent_value, 4)), polarity)
        # result
        return counter

    def _calc_overall_sentiment_for_day(self, max_sent, fb_p_values, fb_c_values, yahoo_values, tw_values):
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
        norm_score = score/math.sqrt((score*score) + alpha)
        return norm_score

    @staticmethod
    def _format_sentiment(norm_score):
        if -0.1 < norm_score < 0.1:
            return 'neu'
        elif norm_score > 0:
            return 'pos'
        elif norm_score < 0:
            return 'neg'

    def _evaluate_results_for_company(self, total_data):
        """For every day and every delay evaluate relation between sentiment value and stock price movement."""
        # Prepare variables
        stats = {}
        for i in [-1, 1, 2, 3]:
            stats[i] = {
                'pos_up': 0.0, 'pos_down': 0.0, 'pos_const': 0.0,
                'neg_up': 0.0, 'neg_down': 0.0, 'neg_const': 0.0,
                'neu_up': 0.0, 'neu_down': 0.0, 'neu_const': 0.0,
            }
        dir_indexes = {3: -2, 2: -3, 1: -4, -1: -5}
        # Process all days
        for day in total_data:
            for i in [-1, 1, 2, 3]:
                stats[i][day[-1] + '_' + day[dir_indexes[i]]] += 1
        # result
        return stats

    def _calc_metrics_from_results(self, id_company):
        """Calculate some metrics from evaluated results (confusion matrix)."""
        # Get company results (all delays).
        results = self.evaluated_results[id_company]
        # Count total number of values in one delay data.
        total_values_count = sum(results.values()[0].values())
        # Process all delays and calculate metrics.
        metrics = {}
        for delay, data in results.items():
            try:
                accuracy = (data['pos_up'] + data['neg_down'] + data['neu_const']) / total_values_count
                precision = data['pos_up'] / (data['pos_up'] + data['pos_down'])
                recall = data['pos_up'] / (data['pos_up'] + data['neg_up'])
            except ZeroDivisionError:
                precision = None
                recall = None
            metrics[delay] = {'accuracy': accuracy, 'precision': precision, 'recall': recall}
        # result
        return metrics

    def _format_metrics_to_list(self, metrics):
        ordered_keys = sorted(metrics.keys())
        lines = []
        for key in ordered_keys:
            m_line = 'delay %d: accuracy: %.4f, ' % (key, metrics[key]['accuracy'])
            m_line += 'precision: ' + str(metrics[key]['precision']) + ', recall: ' + str(metrics[key]['recall'])
            lines.append([m_line])
        # result
        return lines
