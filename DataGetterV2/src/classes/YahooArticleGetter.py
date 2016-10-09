import urllib2
import json
import time
import datetime
import random
import traceback
import socket

from ArticleParser import ArticleParser
from YahooDbModel import YahooDbModel
from MyMailer import MyMailer
from exceptions.ParsingNotImplementedException import ParsingNotImplementedException


class YahooArticleGetter(object):
    """
    Download articles from Yahoo Finance.
    """

    def __init__(self):
        self.headlines_url = 'http://finance.yahoo.com/quote/'
        self.db_model = YahooDbModel()
        self.article_parser = ArticleParser()
        self.exec_error = False

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
                #break   # end script
        # Log execution
        self.db_model.add_log_exec(4, self.exec_error)

    
    def get_headlines(self, ticker, company_id, last_date_in_db):
        """
        Get headlines and save new articles for given company.
        """
        # Get ticker page.
        page = urllib2.urlopen(self.headlines_url + ticker, timeout=5).readlines()
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
            share_data = self.__get_share_count(a_url)
            # Prepare data for saving to DB.
            final_data = self._prepare_article_data_for_db(list_data, parsed_data, share_data)
            print final_data['url']
            if not final_data:
                return True
            #return True
            # Get server ID or Save a new server to DB.
            server_id = self.db_model.get_server_id(a_publisher, a_is_native)
            # Save article to DB.
            article_id = self.db_model.add_article(final_data, company_id, server_id)
            # Save article share count.
            if share_data:
                self.db_model.add_article_history(article_id, share_data['fb_shares'], share_data['tw_shares'])
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
                html = urllib2.urlopen(url, timeout=5).readlines()
                #html = open('../test_data/ya.htm')
                return self.article_parser.parse_native_yahoo(html)
            else:
                print('preview'),
                html = urllib2.urlopen('http://finance.yahoo.com' + preview_link, timeout=5).readlines()
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
        out_data['yahoo_uuid'] = parsed_data['yahoo_uuid'] if 'yahoo_uuid' in parsed_data else None
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

    def get_article_comments(self, days_ago_from, days_ago_to):
        for company in self.db_model.get_companies():
            articles = self.db_model.get_articles_in_interval(company['id'], days_ago_from, days_ago_to)
            url_template = ('http://finance.yahoo.com/_finance_doubledown/api/resource/CommentsService.comments;count=100;'
                            'publisher=finance-en-US;sortBy=highestRated;uuid={yahoo_uuid}?'
                            'bkt=fintest008&device=desktop&feature=&intl=us&lang=en-US&partner=none&region=US&site=finance&'
                            'tz=Europe%2FPrague&ver=0.101.427&returnMeta=true'
                            )
            for article in articles:
                # Get comments from Yahoo
                get_url = url_template.format(yahoo_uuid=article['yahoo_uuid'])
                json_com = urllib2.urlopen(get_url, timeout=5).read()
                comments_data = json.loads(json_com)['data']
                print('comp {0}, {1}, {2} comments'.format(
                    article['company_id'], article['published_date'], comments_data['count'])
                )
                # Get comments already saved in DB
                db_comments = self.db_model.get_comments_for_article(article['id'])
                com_ids_in_db = [x[0] for x in db_comments]
                # Process comments
                self._process_comments_in_article(comments_data, article, com_ids_in_db)
        # Log execution
        self.db_model.add_log_exec(7, False)


    def _process_comments_in_article(self, comments_data, article, com_ids_in_db):
        all_data = []
        for com in comments_data['list']:
            yahoo_id = com['selfURI'].split('/')[-1]
            if yahoo_id in com_ids_in_db:
                continue
            # Prepare data
            content = ''
            for par in com['content']:
                content += '<p>{0}</p>'.format(par.strip())
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
            ]
            # Add data
            all_data.append(save_data)
        # Save all to DB
        if all_data:
            self.db_model.add_comments(all_data)


    ### METHOD 3: article share count

    def __get_share_count(self, url):
        """Get number of shares for given URL on Facebook."""
        return False    # after 20 articles it gives 403 forbidden error
        try:
            # Get FB share count.
            fb_data = json.loads(urllib2.urlopen('http://graph.facebook.com/' + url).read())
            # Check count
            fb_shares = int(fb_data['shares']) if 'shares' in fb_data else 0
            # Is it worth saving?
            if fb_shares == 0:
                return False    # No, it isn't.
            # Prepare result
            return {'fb_shares': fb_shares, 'tw_shares': None}
        except Exception, e:
            print "FB share error: " + str(e)
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


