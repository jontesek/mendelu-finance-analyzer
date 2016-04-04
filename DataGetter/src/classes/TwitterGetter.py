import datetime
import time

from TwitterDbModel import TwitterDbModel
from MyMailer import MyMailer


class TwitterGetter(object):

    def __init__(self, twitter):
        self.twitter_api = twitter          # Twython object
        self.db_model = TwitterDbModel()
        self.exec_error = False


    def get_all_tweets(self, sleep_seconds_n=16):
        """Get all possible tweets for all companies."""
        # Browse all companies
        for company in self.db_model.get_companies():
            print "=====%d: %s=====" % (company['id'], company['tw_search_name'])
            try:
                # If company has no Twiter name, use only search name field.
                if company['tw_name'] == 'NULL':
                    self.__get_search_tweets('search_name', company)
                    continue    # Skip other tweets types.
                # Get tweets containing @companyUsername: @CocaCola
                self.__get_search_tweets('mention', company)
                # Get tweets containg "company name" but not containing @companyUsername: coco cola -@CocaCola
                self.__get_search_tweets('search_name', company)
                # Get tweets which are replies to company tweets: to:CocaCola
                self.__get_search_tweets('reply', company)
                # Get tweets from company timeline
                self.__get_timeline_tweets(company)
            except Exception, e:
                self.exec_error = True
                print "serious error: %s" % repr(e)
                self.__send_serious_error(e)
                break   # end loop
            # Wait some time to obey Twitter API rate limits.
            time.sleep(sleep_seconds_n)
        # Log execution
        self.db_model.add_log_exec(3, self.exec_error)
        
    
    def __get_search_tweets(self, tweet_type, company):
        """Main method for downloading and saving requested tweets."""
        # Get ID of last downloaded tweet.
        last_id = company['tw_'+tweet_type+'_id']
        # Download timestamp
        cur_timestamp = int(time.time()) 
        # Create a correct search query.
        query = self.__create_query(tweet_type, company['tw_name'], company['tw_search_name'])
        # Send request to Twitter and get result.
        result = self.twitter_api.search(q=query, lang='en', result_type='mixed', count=100, since_id=last_id)
        # Check if there are any news tweets.
        if not result['statuses']:
            #print "nothing new"
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
        

    def __create_query(self, tweet_type, comp_username, search_name):
        """Create a search query based on provided tweet type."""  
        if tweet_type == 'mention':
            return '@'+comp_username
        if tweet_type == 'search_name':
            if comp_username == 'NULL':
                return search_name
            else:
                return search_name + ' -@'+comp_username
        if tweet_type == 'reply':
            return 'to:'+comp_username


    def __get_timeline_tweets(self, company):
        """Timeline method for downloading and saving requested tweets."""
        # Get ID of last downloaded tweet.
        last_id = company['tw_timeline_id']
        # Download timestamp
        cur_timestamp = int(time.time())
        # Send request to Twitter and get result.
        try:
            result = self.twitter_api.get_user_timeline(screen_name = company['tw_name'], count = 200, since_id = last_id)
        except Exception, e:
            self.exec_error = True
            print "Timeline problem with company %s" % company['tw_name']
            self.__send_name_error(company['tw_name'], e)
            return True
        # Check if there are any news tweets.
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
        data.append(status['in_reply_to_status_id']) # reply to
        #=== Tweet place
        if status['place'] == None:
            data.append(None)
            data.append(None)
        else:
            data.append(status['place']['name'])
            data.append(status['place']['country_code'])
        # User data
        data.append(status['user']['id'])                    # user id
        data.append(status['user']['followers_count'])       # followers count
        data.append(status['user']['friends_count'])         # number of accounts he follows
        data.append(status['user']['statuses_count'])        # statuses count
        data.append(status['user']['location'])              # location 
        # Download timestamp
        data.append(cur_timestamp)
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
    