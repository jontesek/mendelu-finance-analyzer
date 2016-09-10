from DbModel import DbModel


class TwitterDbModel(DbModel):
    '''
    DB methods for Twitter.
    Parent constructor sets a DB connection ("dbcon" attribute).
    '''

    
    def get_companies(self):
        cursor = self.dbcon.cursor(dictionary=True)
        query = 'SELECT id, ticker, tw_name, tw_search_name, tw_mention_id, tw_search_name_id, tw_reply_id, tw_timeline_id, tw_ticker_id ' \
        'FROM company JOIN last_download ON id = company_id WHERE ticker IS NOT NULL'
        cursor.execute(query)
        return cursor.fetchall()
    
    
    def add_tweets(self, tw_data):
        cursor = self.dbcon.cursor()
        query = "REPLACE INTO tw_status (tw_id, company_id, tweet_type, created_at, favorite_count, retweet_count, text, " \
        "reply_to_status_id, place_name, place_country, user_id, followers_count, friends_count, statuses_count, user_location, download_timestamp, " \
                "entities, contributors, truncated, is_quote_status, retweeted, coordinates, in_reply_to_user_id, lang) " \
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.executemany(query, tw_data)
        #self.dbcon.commit()
        cursor.close()
        
        
    def update_last_id(self, tweet_type, last_id, company_id):
        cursor = self.dbcon.cursor()
        query = 'UPDATE last_download SET tw_'+tweet_type+'_id = %s WHERE company_id = %s'
        cursor.execute(query, (last_id, company_id))
        self.dbcon.commit()
        cursor.close()
