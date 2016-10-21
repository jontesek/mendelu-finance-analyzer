import datetime
import time
import json
import socket

import requests.exceptions
from twython.exceptions import TwythonRateLimitError, TwythonError

from TwitterDbModel import TwitterDbModel
from MyMailer import MyMailer


class TwitterGetter(object):
    """
    Download tweets from Twitter.
    """

    def __init__(self, twitter):
        self.tw_api = twitter          # Twython object
        self.db_model = TwitterDbModel()
        self.exec_error = False


    def get_all_tweets(self):
        """Get all possible tweets for all companies."""
        for company in self.db_model.get_companies():
            print "=====%d: %s=====" % (company['id'], company['tw_search_name'])
            try:
                self._get_tweets_for_company(company)
            except TwythonRateLimitError:
                reset_time = self.tw_api.get_application_rate_limit_status()['resources']['search']['/search/tweets']['reset']
                wait_secs = reset_time - int(time.time()) + 60
                print('Twitter API: need to wait {0} sec ({1} min)'.format(wait_secs, wait_secs / 60))
                time.sleep(wait_secs)
                try:
                    self._get_tweets_for_company(company)
                except TwythonError as e:
                    print str(e)
                    time.sleep(20)
                    try:
                        self._get_tweets_for_company(company)
                    except Exception as e:
                        print str(e)
                        continue
            except TwythonError as e:
                print str(e)
                time.sleep(20)
                self._get_tweets_for_company(company)
            except socket.timeout as e:
                print str(e)
                time.sleep(20)
                self._get_tweets_for_company(company)
            except requests.exceptions.ConnectionError, e:
                print('Twitter connection error: ' + str(e))
                time.sleep(20)
            except Exception, e:
                self.exec_error = True
                print "serious error: %s" % repr(e)
                self.__send_serious_error(e)


    def _get_tweets_for_company(self, company):
        # If company has no Twitter name, use only search name field.
        if not company['tw_name']:
            self.__get_search_tweets('ticker', company)
            self.__get_search_tweets('search_name', company)
            return True
        # Get tweets containing "$ticker": $KO
        self.__get_search_tweets('ticker', company)
        # Get tweets containing @companyUsername: @CocaCola
        self.__get_search_tweets('mention', company)
        # Get tweets containg "company name" but not containing @companyUsername: coca cola -@CocaCola
        self.__get_search_tweets('search_name', company)
        # Get tweets which are replies to company tweets: to:CocaCola
        self.__get_search_tweets('reply', company)
        # Get tweets from company timeline
        self.__get_timeline_tweets(company)


    def __get_search_tweets(self, tweet_type, company):
        """Search - downloading and saving requested tweets."""
        # Get ID of last downloaded tweet.
        last_id = company['tw_'+tweet_type+'_id']
        # Download timestamp
        cur_timestamp = int(time.time()) 
        # Create a correct search query.
        query = self.__create_query(tweet_type, company['tw_name'], company['tw_search_name'], company['ticker'])
        #print query
        # Send request to Twitter and get result.
        result = self.tw_api.search(q=query, lang='en', result_type='mixed', count=100, since_id=last_id)
        # Check if there are any new tweets.
        if not result['statuses']:
            #print('nothing new')
            return True       # skip company
        # Prepare tweets.
        tw_data = []
        for status in reversed(result['statuses']):
            tw_data.append(self.__process_status(status, company['id'], tweet_type, cur_timestamp))
        # Save tweets to DB.
        self.db_model.add_tweets(tw_data)
        # Get new max ID and update DB.
        max_id = result['search_metadata']['max_id']
        self.db_model.update_last_id(tweet_type, max_id, company['id'])
        

    def __create_query(self, tweet_type, comp_username, search_name, ticker):
        """Create a search query based on provided tweet type."""  
        if tweet_type == 'mention':
            return '@'+comp_username
        if tweet_type == 'search_name':
            if not comp_username:
                return search_name
            else:
                return search_name + ' -@'+comp_username
        if tweet_type == 'reply':
            return 'to:'+comp_username
        if tweet_type == 'ticker':
            return '$' + ticker


    def __get_timeline_tweets(self, company):
        """Timeline - downloading and saving requested tweets."""
        # Get ID of last downloaded tweet.
        last_id = company['tw_timeline_id']
        # Download timestamp
        cur_timestamp = int(time.time())
        # Send request to Twitter and get result.
        try:
            result = self.tw_api.get_user_timeline(screen_name=company['tw_name'], count=200, since_id=last_id)
        except Exception, e:
            self.exec_error = True
            print "Timeline problem with company %s" % company['tw_name']
            self.__send_name_error(company['tw_name'], e)
            return False
        # Check if there are any new tweets.
        if not result:
            #print "nothing new"
            return True       # skip company
        # Prepare tweets.
        tw_data = []
        for status in reversed(result):
            tw_data.append(self.__process_status(status, company['id'], 'timeline', cur_timestamp))
        # Save tweets to DB.
        self.db_model.add_tweets(tw_data)
        # Get new max ID and update DB.
        max_id = result[0]['id']
        self.db_model.update_last_id('timeline', max_id, company['id'])


    def __process_status(self, status, company_id, tweet_type, cur_timestamp):
        """Process tweet, get desired information and return list for writing to DB."""
        # for key, value in status.iteritems():
        #     print(">%s: %s") % (key, value)
        # exit()
        data = []
        # Tweet data
        data.append(status['id'])                       # tweet id
        data.append(company_id)                         # company ID
        data.append(self.__get_tw_type_n(tweet_type))   # tweet type ID
        #=== datetime created (UTC)
        data.append(datetime.datetime.strptime(status['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
        #=== statistics
        data.append(status['favorite_count'])       # favorites count
        data.append(status['retweet_count'])        # retweets count
        #=== Process text - remove all whitespace
        text = ' '.join(status['text'].strip().split())
        data.append(text)
        #=== Reply to
        data.append(status['in_reply_to_status_id'])  # reply to
        #=== Tweet place
        if status['place'] == None:
            data.append(None)
            data.append(None)
        else:
            data.append(status['place']['name'])
            data.append(status['place']['country_code'])
        # User data
        data.append(status['user']['id'])
        data.append(status['user']['followers_count'])
        data.append(status['user']['friends_count'])         # number of accounts the user follows
        data.append(status['user']['statuses_count'])        # number of tweets which has the user published
        data.append(status['user']['location'] if status['user']['location'] else None)
        # Download timestamp
        data.append(cur_timestamp)
        # More stuff
        data.append(json.dumps(status['entities']))
        data.append(json.dumps(status['contributors']) if status['contributors'] else None)
        data.append(1 if status['truncated'] else 0)
        data.append(1 if 'quoted_status' in status else 0)
        data.append(1 if 'retweeted_status' in status else 0)  # Is it a retweet?
        data.append(json.dumps(status['coordinates']) if status['coordinates'] else None)
        data.append(status['in_reply_to_user_id'])
        data.append(status['lang'])
        # result
        return data
    
    
    def __get_tw_type_n(self, tw_type):
        if tw_type == 'mention':
            return 1
        elif tw_type == 'search_name':
            return 2
        elif tw_type == 'reply':
            return 3
        elif tw_type == 'timeline':
            return 4
        elif tw_type == 'ticker':
            return 5


    # EMAILING

    def __send_name_error(self, company_name, error):
        print repr(error)
        """Send email to inform about timeline name error from TW API."""
        message = 'Hello,\nthere was a name error while getting twitter data from timeline of company %s.\n' % company_name
        message += repr(error)
        message += '\n\n Please edit the database.'
        message += '\n\nFinance DataGetter from sosna.mendelu.cz'
        MyMailer.send_error_email('Finance DataGetter Twitter error - company', message)
        
    def __send_serious_error(self, error):
        """Send email to inform about serious error from TW API."""
        message = 'Hello,\nthere was a serious error while getting twitter data.\n\n'
        message += repr(error)
        message += '\n\n The script was stopped before ending. Please edit the program.'
        message += '\n\nFinance DataGetter from sosna.mendelu.cz'
        MyMailer.send_error_email('Finance DataGetter Twitter SERIOUS error', message)
    