import urllib2
import json
from bs4 import BeautifulSoup
import re
import datetime
import time
import pytz

from ArticleParser import ArticleParser
from YahooDbModel import YahooDbModel
from MyMailer import MyMailer
from exceptions.ParsingNotImplementedException import ParsingNotImplementedException


class YahooArticleGetter(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.headlines_url = 'http://finance.yahoo.com/q/h?s='
        self.db_model = YahooDbModel()
        self.article_parser = ArticleParser()
        self.exec_error = False
        self.parse_datetime = False
        # Precompiled patterns
        self.native_p = re.compile('^http://finance.yahoo.com/news/.+')
        self.h_time_p = re.compile('.+ (\d+:\d+\w\w) .*')

    #### METHOD 1: get new articles
        
    def get_new_articles(self):
        """Main method for getting and saving new articles."""
        # Browse through all companies.
        for company in self.db_model.get_companies():
            print "====%d: %s====" % (company['id'], company['ticker'])
            # Get headlines and process so far unsaved articles.
            try: 
                self.get_headlines(company['ticker'], company['id'], company['article_newest_saved'])
            except Exception, e:
                self.exec_error = True
                print "serious error: "+repr(e)
                self.__send_serious_error(e)
                break   # end script
        # Log execution.
        self.db_model.add_log_exec(4, self.exec_error)
        
    
    def get_headlines(self, ticker, company_id, last_date):
        """
        Get headlines and save articles for given company.
        :param ticker:
        :param company_id:
        :param last_date:
        :return:
        """
        # Get headlines page
        page = urllib2.urlopen(self.headlines_url+ticker)
        #page = open('../test_data/amd_headlines.htm')
        soup = BeautifulSoup(page, "lxml")
        # Traverse to headlines list
        table = soup.find('table', id='yfncsumtab')
        # Check if ticker page exists.
        if not table:
            self.exec_error = True
            print "not exists"
            self.__send_ticker_error(ticker)
            return False
        # Get headings (dates)
        try:
            headings = table.find_all('tr')[2].td.div.find_all('h3')
        except Exception, e:    # Ticker was moved.
            self.exec_error = True
            print e
            self.__send_ticker_error(ticker)
            return False
        # Newest saved article date
        self.newest_saved_date = False
        last_date = pytz.timezone('America/New_York').localize(last_date)
        # Process headings (dates)
        for heading in headings:
            # Get heading date.
            h_date = datetime.datetime.strptime(heading.span.text, '%A, %B %d, %Y')
            h_date = pytz.timezone('America/New_York').localize(h_date)
            # Check if the date is today or yesterday.
            ny_date = datetime.datetime.now(pytz.timezone('America/New_York')).replace(minute=0, hour=0, second=0, microsecond=0)
            max_date = ny_date - datetime.timedelta(days=1)
            #print "UTC date: %s, MAX date: %s, H date: %s" % (datetime.datetime.utcnow(), max_date, h_date)
            if h_date > max_date:
                print "%s: today - skip the date" % h_date
                continue
            # Check the date against previously newest saved date.
            if h_date <= last_date:
                print "%s: nothing new - end loop" % h_date
                break
            # Process headlines for given date.           
            self.__process_headlines_list(heading.next_sibling.children, company_id, h_date)
        # If something changed, update last download article date and COMMIT all inserts.
        print "NEWEST DATE: %s" % self.newest_saved_date
        if self.newest_saved_date:
            self.db_model.update_last_download(company_id, self.newest_saved_date)

    
    def __process_headlines_list(self, headlines, company_id, h_date):
        # Browse all articles
        for li in headlines:
            try:
                #print li.a.text
                # Select server name
                server = li.cite.contents[0].strip()
                s_name = server[3:] if server[0:2] == 'at' else server 
                # Get article URL
                a_url = li.a['href']
                # Check if article is from native server.
                is_native = self.native_p.match(a_url)
                # Get server ID or Save a new server to DB.
                server_id = self.db_model.get_server_id(s_name, is_native)
                # Parse article
                article = self.__parse_article(a_url, is_native, s_name)
                # Check if article datetime could be parsed.
                if article['datetime']:
                    print '----'+str(article['datetime'])
                    # Convert date from EDT to UTC - add 4 hours (summer) or 5 hours (winter).
                    article['datetime'] = self.convert_edt_to_utc(article['datetime'])
                else:
                    print '----'+str(h_date)
                    article['datetime'] = h_date    # Use heading date.
                # Save article to DB.
                article_id = self.db_model.add_article(article, company_id, a_url, server_id)
                # Is it the first (newest) saved article in the loop?
                if not self.newest_saved_date:
                    self.newest_saved_date = article['datetime'].date()
                # Get and save article history.
                share_data = self.__get_share_count(a_url)
                if share_data:
                    self.db_model.add_article_history(article_id, share_data['fb_shares'], share_data['tw_shares'])
            except urllib2.URLError, e:
                print(e)     # Article url is not accessible.
                continue
            except ParsingNotImplementedException, e:
                print(e)
                continue


    def __parse_article(self, url, is_native, s_name):
        """Parse the article (choose the right parser)."""
        if is_native:
            html = urllib2.urlopen(url)
            #html = open('../test_data/adt_article.htm')
            return self.article_parser.native_yahoo(html, self.parse_datetime)
        else:
            raise ParsingNotImplementedException('Parsing for server '+s_name+' is not implemented.')
        

    #### METHOD 2: update article statistics
       
    def update_article_stats(self, days):
        """Get and save actual number of shares for all articles."""
        # Browse through all companies.
        for company in self.db_model.get_companies_update():
            print "====%s====" % company['id']
            articles_history = []
            cur_timestamp = int(time.time())
            # Get articles and their share data.
            for article in self.db_model.get_articles_since(days, company['id']):
                #print article['id']
                data = self.__get_share_count(article['url'])
                if data:
                    articles_history.append((article['id'], cur_timestamp, data['fb_shares'], data['tw_shares']))
            # Save non-empty share data to DB.
            if articles_history:
                self.db_model.add_articles_history(articles_history) 
            # Wait some time.
            time.sleep(1)
        # Log execution.
        self.db_model.add_log_exec(5, self.exec_error)
    

    def __get_share_count(self, url):
        """Get number of shares for given URL on Facebook."""
        try: 
            # Get FB share count.
            fb_data = json.loads(urllib2.urlopen('http://graph.facebook.com/'+url).read())
            # Twitter share API does not work anymore (from 20.11.2015).
            # Check count
            fb_shares = int(fb_data['shares']) if 'shares' in fb_data else 0
            # Is it worth saving?
            if fb_shares == 0:
                return False    # No, it isn't.
            # Prepare result
            return {'fb_shares': fb_shares, 'tw_shares': None}
        except Exception, e:
            print "Could not get share count: " + e
            return False
    

    ### EMAIL methods
    
    def __send_ticker_error(self, ticker):
        """Send email to inform that the company ticker cannot be found on Yahoo Finance."""
        message = 'Hello,\nthere was an error while downloading articles from Yahoo Finance.\n'
        message += 'Ticker %s does not exist there. Please update the database.' % ticker
        message += '\n\nFinance DataGetter from sosna.mendelu.cz'
        MyMailer.send_error_email('Finance DataGetter Yahoo error - ticker not exists', message)
        
    
    def __send_serious_error(self, exception):
        """Send email to inform about serious error encountered while executing the program."""
        message = 'Hello,\nthere was a serious uncaught error while downloading articles from Yahoo Finance.\n\n'
        message += repr(exception)
        message += '\n\n The program was stopped before ending. Please edit the program.'
        message += '\n\nFinance DataGetter from sosna.mendelu.cz'
        MyMailer.send_error_email('Finance DataGetter Yahoo SERIOUS error', message)
    

    #### OTHER methods
    
    def convert_edt_to_utc(self, edt_datetime):
        """Create UTC datetime from EDT datetime."""
        ny_tz = pytz.timezone('America/New_York')   # define NY timezone
        ny_time = ny_tz.localize(edt_datetime)      # create non naive datetime object 
        utc_time = ny_time.astimezone(pytz.UTC)     # convert it to UTC
        # result 
        return utc_time
    
        