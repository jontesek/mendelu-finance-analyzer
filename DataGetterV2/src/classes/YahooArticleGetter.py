import urllib2
import json
import time
import datetime
import random
import traceback
import socket
from httplib import IncompleteRead

import facebook
import twython

from ArticleParser import ArticleParser
from YahooDbModel import YahooDbModel
from MyMailer import MyMailer
from my_exceptions import ParsingNotImplementedException, AppDataNotFoundRetryException


class YahooArticleGetter(object):
    """
    Download articles from Yahoo Finance.
    """

    def __init__(self, fb_config, tw_config):
        self.headlines_url = 'http://finance.yahoo.com/quote/'
        self.db_model = YahooDbModel()
        self.article_parser = ArticleParser()
        self.exec_error = False
        # Share count
        self.fb_api = facebook.GraphAPI(fb_config['access_token'], version='2.7')
        self.tw_api = twython.Twython(app_key=tw_config['app_key'], access_token=tw_config['access_token'])
        # Yahoo comments
        self.com_url_template = (
                'http://finance.yahoo.com/_finance_doubledown/api/resource/CommentsService.comments;count={com_count};'
                'publisher=finance-en-US;sortBy=highestRated;uuid={yahoo_uuid}?'
                'bkt=fintest008&device=desktop&feature=&intl=us&lang=en-US&partner=none&region=US&site=finance&'
                'tz=Europe%2FPrague&ver=0.101.427&returnMeta=true')

    #### METHOD 1: get new articles
        
    def get_new_articles(self, company_sleep=(10, 15)):
        """Main method for getting and saving new articles for all companies."""
        for company in self.db_model.get_companies():
            print "====%d: %s====" % (company['id'], company['ticker'])
            try:
                self.get_headlines(company['ticker'], company['id'], company['article_newest_saved'])
                time.sleep(random.uniform(company_sleep[0], company_sleep[1]))
            except Exception:
                self.exec_error = True
                print "serious error: {0}".format(traceback.format_exc())
                self.__send_serious_error(traceback.format_exc())
        # Log execution
        self.db_model.add_log_exec(4, self.exec_error)

    
    def get_headlines(self, ticker, company_id, last_date_in_db):
        """
        Get headlines and save new articles for given company.
        """
        # Get ticker page
        ticker_url = self.headlines_url + ticker
        page_html = self._get_content_from_url(ticker_url, True, 3)
        #page = open('../test_data/ticker_not_found.htm').readlines()
        # Check if ticker page exists.
        header_line = page_html[0]
        if '<title></title>' in header_line:
            self.exec_error = True
            print("Ticker %s does not exist.") % ticker
            self.__send_ticker_error(ticker)
            return False
        # Find App Data
        app_data = self._try_to_get_appdata(ticker_url, page_html)
        if not app_data:
            self.exec_error = True
            msg = 'JSON data was not found (ticker %s).'
            print(msg % ticker)
            self.__send_serious_error(msg % ticker)
            return False
        # Get the articles.
        page_name = app_data['context']['dispatcher']['stores']['StreamStore']['pageCategory']
        page_field = '%s.mega' % page_name
        try:
            articles = app_data['context']['dispatcher']['stores']['StreamStore']['streams'][page_field]['data']['stream_items']
        except KeyError, e:
            print "Page key error:" + str(e)
            return False
        # Process all articles (from oldest to newest, 10 articles into history).
        for art in reversed(articles):
            self.__process_article_from_list(art, company_id, last_date_in_db)
        # Commit inserts and update newest saved article datetime.
        self.db_model.update_last_download(company_id)

    
    def __process_article_from_list(self, list_data, company_id, last_date_in_db):
        try:
            # Check if the article can be already in the database.
            article_date = datetime.datetime.utcfromtimestamp(list_data['pubtime'] / 1000)
            print str(article_date),
            if article_date <= last_date_in_db:
                print('not saving!')
                return False
            # Check if the article is advertisement.
            if list_data['type'] == 'ad':
                return False
            # If the article should be parsed, wait some time.
            #time.sleep(random.uniform(2, 4))
            # Define some used variables.
            a_publisher = list_data['publisher'].strip()
            a_is_native = False if list_data['off_network'] else True
            a_url = list_data['url']
            # Parse the article.
            parsed_data = self._try_to_parse_article(a_url, a_is_native, list_data['link'], 3)
            # Get share data.
            share_data = self.__get_share_count(a_url, False)
            # Prepare data for saving to DB.
            final_data = self._prepare_article_data_for_db(list_data, parsed_data, share_data)
            print final_data['url']
            #return True
            # Get server ID or Save a new server to DB.
            server_id = self.db_model.get_server_id(a_publisher, a_is_native)
            # Save article to DB.
            cur_timestamp = int(time.time())
            article_id = self.db_model.add_article(final_data, company_id, server_id, cur_timestamp)
            # Save to article history
            if share_data:
                self.db_model.add_article_history(
                    article_id, cur_timestamp, share_data['fb_shares'], share_data['tw_shares'], final_data['comment_count']
                )
        except ParsingNotImplementedException, e:
            print(e)
        # OK
        return True


    def __parse_article(self, url, is_native, preview_link, max_retries):
        if is_native:
            print('native'),
            html = self._get_content_from_url(url, True, max_retries)
            #html = open('../test_data/ya.htm')
            return self.article_parser.parse_native_yahoo(html) if html else False
        else:
            print('preview'),
            get_url = 'http://finance.yahoo.com' + preview_link
            html = self._get_content_from_url(get_url, True, max_retries)
            #html = open('../test_data/yahoo_preview.htm')
            return self.article_parser.parse_yahoo_preview(html) if html else False


    def _prepare_article_data_for_db(self, list_data, parsed_data, share_data):
        out_data = {}
        # Data from news list
        out_data['title'] = list_data['title']
        out_data['url'] = list_data['url']
        out_data['summary'] = list_data.get('summary', None)
        out_data['published_date'] = datetime.datetime.utcfromtimestamp(list_data['pubtime'] / 1000)
        out_data['off_network'] = list_data['off_network']
        out_data['comment_count'] = list_data.get('commentCount', 0)
        out_data['created_timestamp'] = list_data['pubtime']
        # Parsed data from article
        out_data['yahoo_uuid'] = parsed_data.get('yahoo_uuid', None) if parsed_data else None
        out_data['text'] = parsed_data['text'] if parsed_data else None
        out_data['author_name'] = parsed_data['author_name'] if parsed_data else None
        out_data['author_title'] = parsed_data['author_title'] if parsed_data else None
        out_data['j_entities'] = parsed_data['j_entities'] if parsed_data else None
        out_data['j_tags'] = parsed_data['j_tags'] if parsed_data else None
        out_data['doc_type'] = parsed_data['doc_type'] if parsed_data else None
        out_data['article_body_data'] = parsed_data.get('article_body_data', None) if parsed_data else None
        out_data['paragraph_count'] = parsed_data['paragraph_count'] if parsed_data else None
        out_data['word_count'] = parsed_data['word_count'] if parsed_data else None
        # Share data
        out_data['fb_shares'] = share_data['fb_shares'] if share_data else 0
        out_data['tw_shares'] = share_data['tw_shares'] if share_data else 0
        # Final result
        return out_data

    ## Reading methods

    def _try_to_get_appdata(self, url, first_html, max_retries=3):
        try:
            return self._get_appdata_from_html(first_html)
        except AppDataNotFoundRetryException as e:
            print str(e)

            while max_retries:
                print "appdata_" + str(max_retries),
                try:
                    new_html = self._get_content_from_url(url, True)
                    return self._get_appdata_from_html(new_html)
                except AppDataNotFoundRetryException as e:
                    print str(e)
                    max_retries -= 1
        return False


    def _try_to_parse_article(self, url, is_native, preview_link, max_retries):
        while max_retries:
            print('parse_{0}'.format(max_retries)),
            try:
                return self.__parse_article(url, is_native, preview_link, max_retries)
            except AppDataNotFoundRetryException as e:
                print str(e)
                max_retries -= 1
        return False


    def _get_content_from_url(self, url, lines_to_list, max_retries=3):
        while max_retries:
            print ">>HTTP GET retry = {0}: {1}".format(max_retries, url)
            try:
                connection = urllib2.urlopen(url)
                return connection.readlines() if lines_to_list else connection.read()
            except urllib2.URLError as e:
                print str(e)
                return False
            except socket.timeout as e:
                print str(e)
                max_retries -= 1
            except IncompleteRead as e:
                print str(e)
                max_retries -= 1
        return False


    def _get_appdata_from_html(self, html_lines):
        app_data = None
        for line in html_lines:
            if line.lstrip().startswith('root.App.main'):
                app_data = line[16:-2]
                break
        if app_data:
            return json.loads(app_data)
        else:
            raise AppDataNotFoundRetryException('JSON not found in article')


    #### METHOD 2: get article comments

    def get_article_comments(self, days=7, company_delay_secs=0):
        """
        Get TOP 100 comments for every article published in last X days.
        """
        for company in self.db_model.get_companies():
            print "====%d: %s====" % (company['id'], company['ticker'])
            articles = self.db_model.get_articles_since(days, company['id'], True)
            for article in articles:
                # Get comments from Yahoo
                get_url = self.com_url_template.format(yahoo_uuid=article['yahoo_uuid'], com_count=100)
                try:
                    json_com = self._get_content_from_url(get_url, False, 3)
                except Exception as e:
                    print str(e)
                    continue
                comments_data = json.loads(json_com)['data']
                if comments_data['count']:
                    print('art {0}, comments: {1}'.format(article['id'], comments_data['count']))
                    # Get comments already saved in DB
                    db_comments = self.db_model.get_comments_for_article(article['id'])
                    db_com_dict = {fb_id: db_id for (db_id, fb_id) in db_comments} if db_comments else {}
                    # Process comments
                    self._process_comments_in_article(comments_data, article, db_com_dict)
                    self.db_model.dbcon.commit()

            time.sleep(company_delay_secs)

        # Log execution
        self.db_model.add_log_exec(7, False)


    def _process_comments_in_article(self, comments_data, article, db_com_dict):
        cur_timestamp = int(time.time())

        com_history = []

        for com in comments_data['list']:
            yahoo_id = com['selfURI'].split('/')[-1]

            # If comment is already in DB, save comment history.
            if yahoo_id in db_com_dict:
                com_history.append((
                    db_com_dict[yahoo_id],
                    article['id'],
                    article['company_id'],
                    yahoo_id,
                    com['replyCount'],
                    com['thumbsDownCount'],
                    com['thumbsUpCount'],
                    cur_timestamp,
                ))
                continue

            content = '<p>'.join([x.strip() for x in com['content']])
            content = ' '.join(content.strip().split())     # remove all whitespace (single space remains)

            save_data = [
                article['id'],
                article['company_id'],
                datetime.datetime.utcfromtimestamp(com['createTime'] / 1000),
                yahoo_id,
                content,
                com['replyCount'],
                com['thumbsDownCount'],
                com['thumbsUpCount'],
                com['creator'],
                com['userProfile']['nickName'],
                cur_timestamp,
                com['createTime'],
                len(com['content']),
                len(content.replace('<p>', ' ').split()),
            ]
            new_comment_id = self.db_model.add_comment(save_data)
            com_history.append((
                new_comment_id,
                article['id'],
                article['company_id'],
                yahoo_id,
                com['replyCount'],
                com['thumbsDownCount'],
                com['thumbsUpCount'],
                cur_timestamp,
            ))

        self.db_model.add_comments_history(com_history)


    ### METHOD 3: article share and comment count

    def update_article_stats(self, days, days_interval=None):
        """Get and save actual number of shares and comments for all articles."""
        # Browse through all companies.
        for company in self.db_model.get_companies_for_update():
            print "====%d: %s====" % (company['id'], company['ticker'])
            articles_history = []
            # Get articles and their share and comment data.
            if days_interval:
                articles = self.db_model.get_articles_in_interval(company['id'], days_interval[0], days_interval[1], False)
            else:
                articles = self.db_model.get_articles_since(days, company['id'], False)
            for article in articles:
                #print article['id']
                data = self.__get_share_count(article['url'], article['yahoo_uuid'])
                if data:
                    print article['id'], data
                    articles_history.append((
                        article['id'], data['download_ts'], data['fb_shares'], data['tw_shares'], data['yahoo_comments']
                    ))
            # Save non-empty share data to DB.
            if articles_history:
                self.db_model.add_articles_history(articles_history)
            # Wait some time.
            time.sleep(1)
        # Log execution.
        self.db_model.add_log_exec(5, self.exec_error)


    def __get_share_count(self, url, yahoo_id):
        """Get number of shares for given URL on Facebook and Twitter plus number of Yahoo comments"""
        try:
            # Get Twitter share count
            try:
                tw_data = self.tw_api.search(q=url, lang='en', result_type='mixed', count=100)
            except twython.exceptions.TwythonRateLimitError:
                reset_time = self.tw_api.get_application_rate_limit_status()['resources']['search']['/search/tweets']['reset']
                wait_secs = reset_time - int(time.time()) + 5
                print('Twitter API: need to wait {0} secs ({1} min)'.format(wait_secs, wait_secs / 60))
                time.sleep(wait_secs)
                tw_data = self.tw_api.search(q=url, lang='en', result_type='mixed', count=100)
            tw_shares = len(tw_data['statuses'])
            # Get FB share count
            fb_data = self.fb_api.get_object(url)
            if 'share' in fb_data:
                fb_shares = fb_data['share']['share_count']
            else:
                fb_shares = 0
            # Get Yahoo comments count
            if yahoo_id:
                get_url = self.com_url_template.format(yahoo_uuid=yahoo_id, com_count=1)
                try:
                    yahoo_comments = json.loads(self._get_content_from_url(get_url, False, 3))['data']['count']
                except Exception as e:
                    print str(e)
                    yahoo_comments = None
            else:
                yahoo_comments = None
            # Is it worth saving?
            if fb_shares == 0 and tw_shares == 0 and not yahoo_comments:
                return False    # No, it isn't.
            # Prepare result
            return {
                'download_ts': int(time.time()),
                'fb_shares': fb_shares, 'tw_shares': tw_shares, 'yahoo_comments': yahoo_comments
            }
        except Exception as e:
            print "Share error: " + e
            return False


    ### EMAIL methods
    
    def __send_ticker_error(self, ticker):
        """Send email to inform that the company ticker cannot be found on Yahoo Finance."""
        message = 'Hello,\nthere was an error while downloading articles from Yahoo Finance.\n'
        message += 'Ticker %s does not exist there. Please update the database.' % ticker
        message += '\n\nFinance DataGetter from sosna.mendelu.cz'
        MyMailer.send_error_email('Finance DataGetter Yahoo error - ticker not exists', message)
        
    
    def __send_serious_error(self, error_description):
        """Send email to inform about serious error encountered while executing the program."""
        message = 'Hello,\nthere was a serious uncaught error while downloading articles from Yahoo Finance.\n\n'
        message += error_description
        message += '\n\n The program was stopped before ending. Please edit the program.'
        message += '\n\nFinance DataGetter from sosna.mendelu.cz'
        MyMailer.send_error_email('Finance DataGetter Yahoo SERIOUS error', message)


