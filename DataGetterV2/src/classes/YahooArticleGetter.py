import urllib2
import json
import time
import datetime
import random
import traceback
import socket

import facebook
import twython

from ArticleParser import ArticleParser
from YahooDbModel import YahooDbModel
from MyMailer import MyMailer
from exceptions.ParsingNotImplementedException import ParsingNotImplementedException


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
        self.article_count = 0
        # Yahoo comments
        self.com_url_template = (
                'http://finance.yahoo.com/_finance_doubledown/api/resource/CommentsService.comments;count=100;'
                'publisher=finance-en-US;sortBy=highestRated;uuid={yahoo_uuid}?'
                'bkt=fintest008&device=desktop&feature=&intl=us&lang=en-US&partner=none&region=US&site=finance&'
                'tz=Europe%2FPrague&ver=0.101.427&returnMeta=true')

    #### METHOD 1: get new articles
        
    def get_new_articles(self, company_sleep=(10, 20)):
        """Main method for getting and saving new articles for all companies."""
        for company in self.db_model.get_companies():
            print "====%d: %s====" % (company['id'], company['ticker'])
            try:
                self.get_headlines(company['ticker'], company['id'], company['article_newest_saved'])
                time.sleep(random.uniform(company_sleep[0], company_sleep[1]))
            except Exception:
                self.exec_error = True
                print "serious error: {0}".format(traceback.format_exc())
                #self.__send_serious_error(traceback.format_exc())
        # Log execution
        self.db_model.add_log_exec(4, self.exec_error)

    
    def get_headlines(self, ticker, company_id, last_date_in_db):
        """
        Get headlines and save new articles for given company.
        """
        # Get ticker page
        try:
            page = urllib2.urlopen(self.headlines_url + ticker, timeout=10).readlines()
        except socket.timeout as e:
            print str(e)
            return False
        #page = open('../test_data/ticker_not_found.htm').readlines()
        # Check if ticker page exists.
        header_line = page[0]
        if '<title></title>' in header_line:
            self.exec_error = True
            self.__send_ticker_error(ticker)
            print("Ticker %s does not exist.") % ticker
            return False
        # Find JSON data.
        app_data = None
        for p_line in page:
            if p_line.lstrip().startswith('root.App.main'):
                app_data = p_line[16:-2]
                break
        if not app_data:
            self.exec_error = True
            print('JSON data was not found (ticker %s).') % ticker
            self.__send_serious_error('JSON data was not found (ticker %s).' % ticker)
            return False
        # Read data into dictionary.
        json_data = json.loads(app_data)
        # Get the articles.
        page_name = json_data['context']['dispatcher']['stores']['StreamStore']['pageCategory']
        page_field = '%s.mega' % page_name
        try:
            articles = json_data['context']['dispatcher']['stores']['StreamStore']['streams'][page_field]['data']['stream_items']
        except KeyError, e:
            print str(e)
            return False
        # Process all articles (from oldest to newest, 10 articles into history).
        for art in reversed(articles):
            self.__process_article_from_list(art, company_id, last_date_in_db)
        # Commit inserts and update newest saved article datetime.
        self.db_model.update_last_download(company_id)

    
    def __process_article_from_list(self, list_data, company_id, last_date_in_db):
        try:
            # Check if the article can be already in the database.
            article_date = datetime.datetime.utcfromtimestamp(list_data['pubtime'] / 1000.0)
            print str(article_date),
            if article_date <= last_date_in_db:
                print('not saving!')
                return False
            # Check if the article is advertisement.
            if list_data['type'] == 'ad':
                return False
            # If the article should be parsed, wait some time.
            time.sleep(random.uniform(2, 4))
            # Define some used variables.
            a_publisher = list_data['publisher'].strip()
            a_is_native = False if list_data['off_network'] else True
            a_url = list_data['url']
            # Parse the article.
            parsed_data = self.__parse_article(a_url, a_is_native, list_data['link'])
            # Get share data.
            share_data = self.__get_share_count(a_url, False)
            # Prepare data for saving to DB.
            final_data = self._prepare_article_data_for_db(list_data, parsed_data, share_data)
            print final_data['url']
            if not final_data:
                return True
            #return True
            # Get server ID or Save a new server to DB.
            server_id = self.db_model.get_server_id(a_publisher, a_is_native)
            # Save article to DB.
            cur_ts = int(time.time())
            article_id = self.db_model.add_article(final_data, company_id, server_id, cur_ts)
            # Save article share count.
            if share_data:
                self.db_model.add_article_history(
                    article_id, cur_ts, share_data['fb_shares'], share_data['tw_shares'], final_data['comment_count']
                )
        except urllib2.URLError, e:
            print(e)     # Article URL is not accessible.
        except ParsingNotImplementedException, e:
            print(e)
        # OK
        return True


    def __parse_article(self, url, is_native, preview_link):
        try:
            if is_native:
                print('native'),
                html = urllib2.urlopen(url, timeout=10).readlines()
                #html = open('../test_data/ya.htm')
                return self.article_parser.parse_native_yahoo(html)
            else:
                print('preview'),
                html = urllib2.urlopen('http://finance.yahoo.com' + preview_link, timeout=10).readlines()
                #html = open('../test_data/yahoo_preview.htm')
                return self.article_parser.parse_yahoo_preview(html)
        except socket.timeout as e:
            print str(e)
            return False


    def _prepare_article_data_for_db(self, list_data, parsed_data, share_data):
        out_data = {}
        # Data from news list
        out_data['title'] = list_data['title']
        out_data['url'] = list_data['url']
        out_data['summary'] = list_data.get('summary', None)
        out_data['published_date'] = datetime.datetime.utcfromtimestamp(list_data['pubtime'] / 1000.0)
        out_data['off_network'] = list_data['off_network']
        out_data['comment_count'] = list_data['commentCount'] if 'commentCount' in list_data else 0
        # Parsed data from article
        out_data['yahoo_uuid'] = parsed_data['yahoo_uuid'] if parsed_data and 'yahoo_uuid' in parsed_data else None
        out_data['text'] = parsed_data['text'] if parsed_data else None
        out_data['author_name'] = parsed_data['author_name'] if parsed_data else None
        out_data['author_title'] = parsed_data['author_title'] if parsed_data else None
        out_data['j_entities'] = parsed_data['j_entities'] if parsed_data else None
        out_data['j_tags'] = parsed_data['j_tags'] if parsed_data else None
        out_data['doc_type'] = parsed_data['doc_type'] if parsed_data else None
        # Share data
        out_data['fb_shares'] = share_data['fb_shares'] if share_data else 0
        out_data['tw_shares'] = share_data['tw_shares'] if share_data else 0
        # Final result
        return out_data


    #### METHOD 2: get article comments

    def get_article_comments(self, days_ago_from, days_ago_to, company_delay_secs=0):
        for company in self.db_model.get_companies():
            articles = self.db_model.get_articles_in_interval(company['id'], days_ago_from, days_ago_to)
            for article in articles:
                # Get comments from Yahoo
                get_url = self.com_url_template.format(yahoo_uuid=article['yahoo_uuid'])
                try:
                    json_com = urllib2.urlopen(get_url, timeout=10).read()
                except Exception as e:
                    print str(e)
                    continue
                comments_data = json.loads(json_com)['data']
                print('comp {0}, {1}, {2} comments'.format(
                    article['company_id'], article['published_date'], comments_data['count'])
                )
                # Get comments already saved in DB
                db_comments = self.db_model.get_comments_for_article(article['id'])
                com_ids_in_db = [x[0] for x in db_comments]
                # Process comments
                self._process_comments_in_article(comments_data, article, com_ids_in_db)
                self.db_model.dbcon.commit()

            time.sleep(company_delay_secs)

        # Log execution
        self.db_model.add_log_exec(7, False)


    def _process_comments_in_article(self, comments_data, article, com_ids_in_db):
        cur_timestamp = int(time.time())

        for com in comments_data['list']:
            yahoo_id = com['selfURI'].split('/')[-1]
            if yahoo_id in com_ids_in_db:
                continue

            content = '<p>'.join(com['content'])
            content = ' '.join(content.strip().split())

            save_data = [
                article['id'],
                article['company_id'],
                int(com['createTime'] / 1000),
                yahoo_id,
                content,
                com['replyCount'],
                com['thumbsDownCount'],
                com['thumbsUpCount'],
                com['creator'],
                com['userProfile']['nickName'],
                cur_timestamp,
            ]
            self.db_model.add_comment(save_data)



    ### METHOD 3: article share count

    def update_article_shares(self, days):
        """Get and save actual number of shares for all articles."""
        # Browse through all companies.
        for company in self.db_model.get_companies_update():
            print "====%s====" % company['id']
            articles_history = []
            # Get articles and their share data.
            for article in self.db_model.get_articles_since(days, company['id']):
                #print article['id']
                data = self.__get_share_count(article['url'], article['yahoo_uuid'])
                if data:
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
        """Get number of shares for given URL on Facebook and Twitter."""
        try:
            # Get Twitter share count
            try:
                tw_data = self.tw_api.search(q=url, lang='en', result_type='mixed', count=100)
            except twython.exceptions.TwythonRateLimitError:
                reset_time = self.tw_api.get_application_rate_limit_status()['resources']['search']['/search/tweets']['reset']
                wait_secs = reset_time - int(time.time()) + 5
                print('Twitter API: need to wait {0} seconds ({1})'.format(wait_secs, wait_secs / 60))
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
                get_url = self.com_url_template.format(yahoo_uuid=yahoo_id)
                try:
                    yahoo_comments = json.loads(urllib2.urlopen(get_url, timeout=10).read())['data']['count']
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
        except Exception, e:
            print "Share error: " + str(e)
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


