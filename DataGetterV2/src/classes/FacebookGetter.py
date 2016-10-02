import time
from urllib2 import URLError
import traceback
import json

from facebook import GraphAPIError

from FacebookDbModel import FacebookDbModel
from MyMailer import MyMailer


class FacebookGetter(object):
    """
    Download documents from Facebook.
    """

    def __init__(self, fb_api):
        self.fb_api = fb_api 
        self.db_model = FacebookDbModel()
        self.exec_error = False

        # Generate query for posts
        basic_fields = ('id,created_time,message,shares,type,status_type,story,'
                        'likes.limit(0).summary(true),comments.limit(100).summary(true)'
                        '{id,created_time,message,from,likes.limit(0).summary(true)},')
        reactions_list = [
            'reactions.type({0}).limit(0).summary(total_count).as(reactions_{1})'
            .format(r_type, r_type.lower()) for r_type in ['LOVE', 'WOW', 'HAHA', 'SAD', 'ANGRY', 'THANKFUL']
        ]
        self.posts_query_fields = basic_fields + ','.join(reactions_list)
        
    
    #### METHOD 1: get new posts
    
    def get_new_posts(self):
        """Get new posts and their comments for every company."""
        # Get posts for every company.
        for company in self.db_model.get_companies():
            try:
                self.__get_posts_for(company)
            except Exception:
                self.exec_error = True
                print "serious error: {0}".format(traceback.format_exc())
                #self.__send_serious_error(traceback.format_exc(), company['fb_page'], 'get_new_posts')
                break   # end the cycle
        # Log execution.
        self.db_model.add_log_exec(1, self.exec_error)
    
    
    def __get_posts_for(self, company):
        # Show company
        print "====%d: %s====" % (company['id'], company['fb_page'])
        # Send request to FB.
        try: 
            result = self.fb_api.get_connections(id=company['fb_page'], connection_name='posts', limit=90,
                                                 date_format='U', since=company['fb_post_timestamp'], fields='id')
            #result = json.load(open('../test_data/fb_posts.json'))
        # There was no or wrong response from FB.
        except GraphAPIError, e:
            self.exec_error = True
            print "MYER", str(e)
            # Get error code
            error_code = int(e.result['error']['code'])
            # OK errors: unsupported get request, unknown error 
            if error_code in [100, 1]:
                self.exec_error = False
                return True     # skip company
            # Name error?
            if error_code == 803 or error_code == 21:
                print "Name problem with company %s" % company['fb_page']
                self.__send_name_error(company['fb_page'], e.result['error'], 'get_new_posts')
                return True     # skip company
            # Limit error? Specific for cocacola.
            if error_code == -3:
                #return True
                print "lower the limit please"
                # Lower limit and continue below.
                result = self.fb_api.get_connections(id=company['fb_page'], connection_name='posts', limit=30,
                                                     date_format='U', since=company['fb_post_timestamp'], fields='id')
            # If other than OK errors, send serious message and end the script.
            if error_code not in [100, 1, -3]:
                print "Serious problem with company %s" % company['fb_page']
                self.__send_serious_error(e.result['error'], company['fb_page'], '__get_posts_for')
                raise e
        # Check if it was network unreachable error.
        except URLError, e:
            print(repr(e))
            return True     # skip company
        # Check if there is at least one new post.
        posts = result['data']
        if not posts:
            print "nothing new"
            return True 
        # If there are any new posts, send a new query.
        post_ids = [p['id'] for p in posts]
        posts_dict = self.fb_api.get_objects(ids=post_ids, date_format='U', fields=self.posts_query_fields)
        posts_list = sorted(posts_dict.values(), key=lambda x: x['created_time'])
        self.__process_new_posts(posts_list, company['id'])

    
    def __process_new_posts(self, posts, company_id):
        # Variables for multiple inserts
        posts_history = []
        comments_history = []
        # Timestamp for history insert
        current_timestamp = int(time.time())
        # Go through all posts (from oldest to newest).
        for post in posts:
            # Check if it's a regular post. If not, skip it.
            if 'message' not in post or 'shares' not in post or 'likes' not in post:
                continue
            # Add post to DB
            post_db_id = self.db_model.add_post([
                post['id'], company_id, post['created_time'],
                post['message'].strip(),
                post['likes']['summary']['total_count'],
                post['type'], post['status_type'],
                post.get('story', None),
            ])
            #print "POST ID %s" % post_db_id
            # Save posts history
            posts_history.append([
                post_db_id, post['id'], company_id, current_timestamp,
                post['likes']['summary']['total_count'],
                post['shares']['count'],
                post['comments']['summary']['total_count'],
                post['reactions_love']['summary']['total_count'],
                post['reactions_wow']['summary']['total_count'],
                post['reactions_haha']['summary']['total_count'],
                post['reactions_sad']['summary']['total_count'],
                post['reactions_angry']['summary']['total_count'],
                post['reactions_thankful']['summary']['total_count'],
            ])
            # Process and save comments to the post.
            for com in post['comments']['data']:
                # Add comment
                comment_db_id = self.db_model.add_comment(self.__process_comment(com, post_db_id, company_id))
                # Save comments history
                comments_history.append([
                    comment_db_id, com['id'], company_id, current_timestamp,
                    com['likes']['summary']['total_count'],
                ])
        # Save history to DB
        self.db_model.add_posts_history(posts_history)
        if comments_history:
            self.db_model.add_comments_history(comments_history)
        # Update last download
        self.db_model.update_last_download(company_id, current_timestamp)

    
    #### METHOD 2: check posts
        
    def update_posts(self, days):
        """Update likes for posts and comments (might add new comments)."""
        # Go through all companies.
        for company in self.db_model.get_companies_update():
            try:
                self.__update_posts_for(company, days)
            except Exception:
                self.exec_error = True
                print "serious error: {0}".format(traceback.format_exc())
                self.__send_serious_error(traceback.format_exc(), company['fb_page'], 'update_posts')
                break   # end the cycle
        # Log execution.
        self.db_model.add_log_exec(2, self.exec_error)
    
    
    def __update_posts_for(self, company, days):
        print "====%d====" % company['id']
        # Timestamp for history insert
        current_timestamp = int(time.time())
        # History insert variables
        posts_history = []
        comments_history = []
        # Select posts for given company from last X days.
        for post_db in self.db_model.get_posts_since(days, company['id']):
            #print post_db['id']
            # Get post data from FB.
            try:
                post_data = self.fb_api.get_object(id=post_db['fb_id'], date_format='U', fields=self.posts_query_fields)
            except GraphAPIError, e:
                self.exec_error = True
                print traceback.format_exc()
                # Is it Invalid OAuth access token?
                if int(e.result['error']['code']) == 190:
                    self.__send_serious_error("Invalid access token. \n" + traceback.format_exc(),
                                              company['fb_page'], 'update_posts')
                    raise e    # end script
                # ELSE - skip the post
                continue
            # Skip weird posts (should not be necessary).
            if 'shares' not in post_data or 'likes' not in post_data:
                continue
            # Save post history
            posts_history.append([
                post_db['id'], post_db['fb_id'], company['id'], current_timestamp,
                post_data['likes']['summary']['total_count'],
                post_data['shares']['count'],
                post_data['comments']['summary']['total_count'],
                post_data['reactions_love']['summary']['total_count'],
                post_data['reactions_wow']['summary']['total_count'],
                post_data['reactions_haha']['summary']['total_count'],
                post_data['reactions_sad']['summary']['total_count'],
                post_data['reactions_angry']['summary']['total_count'],
                post_data['reactions_thankful']['summary']['total_count'],
            ])
            # Has post any comments?
            if not post_data['comments']['data']:
                #print('no comments')
                continue    # If not, skip the post.
            # Get DB comments for post
            db_comments = self.db_model.get_comments_for_post(post_db['id'])
            # Create dictionary from comments
            db_com_dict = {fb_id: db_id for (db_id, fb_id) in db_comments}
            #print db_com_dict
            # Process FB comments
            for fb_com in post_data['comments']['data']:
                # Check if comment with the FB ID is already in DB.
                if fb_com['id'] in db_com_dict:
                    # YES - only add item to history.
                    comments_history.append(
                        (db_com_dict[fb_com['id']], fb_com['id'], company['id'], current_timestamp,
                         fb_com['likes']['summary']['total_count'])
                    )
                else:
                    # NO - insert comment into DB, get ID and add item to history.
                    new_comment_id = self.db_model.add_comment(self.__process_comment(fb_com, post_db['id'], company['id']))
                    comments_history.append(
                        (new_comment_id, fb_com['id'], company['id'], current_timestamp,
                         fb_com['likes']['summary']['total_count'])
                    )
        # Save history to DB and commit all.
        if posts_history:
            self.db_model.add_posts_history(posts_history)
        if comments_history:
            self.db_model.add_comments_history(comments_history)
        self.db_model.dbcon.commit()


    #### METHOD 3: page feed

    def get_new_feed_items(self):
        """Get new items from feed for every company."""
        for company in self.db_model.get_companies():
            try:
                self.__get_feed_items_for(company)
                if company['id'] == 4:
                    break
            except Exception:
                self.exec_error = True
                print "serious error: {0}".format(traceback.format_exc())
                #self.__send_serious_error(traceback.format_exc(), company['fb_page'], 'get_new_posts')
                break   # end the cycle
        # Log execution.
        self.db_model.add_log_exec(6, self.exec_error)


    def __get_feed_items_for(self, company):
        query_fields = ('message,story,created_time,id,place,link,type,from,message_tags,shares,status_type,to,'
                        'likes.limit(0).summary(true),comments.limit(0).summary(true)')
        print "====%d: %s====" % (company['id'], company['fb_page'])
        # Send request to FB.
        try:
            result = self.fb_api.get_connections(id=company['fb_page'], connection_name='feed', limit=90,
                                                 date_format='U', since=company['fb_feed_timestamp'], fields=query_fields)
        # There was no or wrong response from FB.
        except GraphAPIError, e:
            self.exec_error = True
            print "MYER", str(e)
            # Get error code
            error_code = int(e.result['error']['code'])
            # OK errors: unsupported get request, unknown error
            if error_code in [100, 1]:
                self.exec_error = False
                return True     # skip company
            # Name error?
            if error_code == 803 or error_code == 21:
                print "Name problem with company %s" % company['fb_page']
                self.__send_name_error(company['fb_page'], e.result['error'], 'get_new_posts')
                return True     # skip company
            # Limit error? Specific for cocacola.
            if error_code == -3:
                #return True
                print "lower the limit please"
                # Lower limit and continue below.
                result = self.fb_api.get_connections(id=company['fb_page'], connection_name='feed', limit=30,
                                                     date_format='U', since=company['fb_feed_timestamp'], fields=query_fields)
            # If other than OK errors, send serious message and end the script.
            if error_code not in [100, 1, -3]:
                print "Serious problem with company %s" % company['fb_page']
                self.__send_serious_error(e.result['error'], company['fb_page'], '__get_posts_for')
                raise e
        # Check if it was network unreachable error.
        except URLError, e:
            print(repr(e))
            return True     # skip company
        # Check if there is at least one new post.
        items = result['data']
        if not items:
            print "nothing new"
            return True
        # If there are any new posts, send a new query.
        self.__process_new_feed_items(items, company['id'])


    def __process_new_feed_items(self, items, company_id):
        current_timestamp = int(time.time())
        # Go through all items (from oldest to newest).
        for item in reversed(items):
            self.db_model.add_feed_item([
                item['id'], company_id, item['created_time'],
                item['message'].strip() if item.get('message', None) else None,
                item['likes']['summary']['total_count'],
                current_timestamp,
                item['shares']['count'] if item.get('shares') else None,
                item['comments']['summary']['total_count'],
                item['type'], item['status_type'],
                item['from'].get('name', None), item['from'].get('id', None),
                item.get('story', None), item.get('link', None),
                json.dumps(item.get('to', None)) if item.get('to', None) else None,
                json.dumps(item.get('message_tags', None)) if item.get('message_tags', None) else None,
                json.dumps(item.get('place', None)) if item.get('place', None) else None,
            ])
        # Update last download
        self.db_model.update_last_download_feed(company_id, current_timestamp)

    
    #### PROCESSING methods
    
    def __process_comment(self, comment, post_db_id, company_id):
        #c_text = ' '.join(comment['message'].strip().split())
        c_text = comment['message'].strip()
        a_name = comment['from']['name'] if 'name' in comment['from'] else None
        data = [
            comment['id'], post_db_id, company_id, comment['created_time'], c_text, comment['from']['id'], a_name,
            comment['likes']['summary']['total_count'],
        ]
        return data
    
    
    #### EMAIL sending methods
    
    def __send_name_error(self, company_name, error, source):
        """Send email to inform about name error from FB API."""
        message = 'Hello,\nthere was a name error while getting facebook data for company %s.\n' % company_name
        message += 'Source: %s \n\n' % source
        message += repr(error)
        message += '\n\n Please edit the database.'
        message += '\n\nFinance DataGetter from sosna.mendelu.cz'
        MyMailer.send_error_email('Finance DataGetter Facebook error - company', message)  
        
    
    def __send_serious_error(self, error_trace, company, source):
        """Send email to inform about serious error in Facebook script."""
        message = 'Hello,\nthere was a serious error while getting facebook data.\n'
        message += 'description: %s, %s \n\n' % (company, source)
        message += error_trace
        message += '\n\n The script was stopped before ending. Please edit the program.'
        message += '\n\nFinance DataGetter from sosna.mendelu.cz'
        MyMailer.send_error_email('Finance DataGetter Facebook SERIOUS error', message)
        