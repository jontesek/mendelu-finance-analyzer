from DbModel import DbModel


class FacebookDbModel(DbModel):
    """
    DB methods for Facebook.
    Parent constructor sets a DB connection ("dbcon" attribute).
    """

    ##### READ methods    
        
    def get_companies(self):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id, fb_page, fb_post_timestamp, fb_feed_timestamp FROM company " \
                "JOIN last_download ON id=company_id WHERE fb_page IS NOT NULL ORDER BY id ASC"
        cursor.execute(query)
        return cursor.fetchall()
    
    
    def get_companies_update(self):
        cursor = self.dbcon.cursor(dictionary=True)
        cursor.execute("SELECT id, fb_page FROM company WHERE fb_page IS NOT NULL ORDER BY id ASC")
        return cursor.fetchall()
    
    
    def get_posts_since(self, days, company_id):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id, fb_id, company_id FROM fb_post WHERE company_id = %s AND created_timestamp >= (UNIX_TIMESTAMP() - %s)"
        cursor.execute(query, [company_id, self.__days_to_seconds(days)])
        return cursor.fetchall()
    
    
    def __days_to_seconds(self, days):
        return days*24*3600
    
    
    def get_comments_for_post(self, post_id):
        cursor = self.dbcon.cursor()
        query = 'SELECT id, fb_id FROM fb_comment WHERE post_id = %s'
        cursor.execute(query, [post_id])
        #print cursor.statement
        return cursor.fetchall()
    
    
    ##### WRITE methods                
    
    def add_post(self, post_data):
        cursor = self.dbcon.cursor()
        query = "INSERT INTO fb_post (fb_id, company_id, created_timestamp, text, init_likes_count, object_type, status_type, story, downloaded_timestamp) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, post_data)  
        return cursor.lastrowid
    
    
    def add_comment(self, com_data):
        cursor = self.dbcon.cursor()
        query = "INSERT INTO fb_comment (fb_id, post_id, company_id, created_timestamp, text, author_fb_id, author_name, init_likes_count, downloaded_timestamp) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, com_data)  
        return cursor.lastrowid
    
    
    def add_posts_history(self, posts_history):
        cursor = self.dbcon.cursor()
        query = ("INSERT INTO fb_post_history (post_id, fb_post_id, company_id, download_timestamp, "
                 "likes_count, shares_count, comments_count, "
                 "reactions_love, reactions_wow, reactions_haha, reactions_sad, reactions_angry, reactions_thankful)"
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.executemany(query, posts_history)
        cursor.close()
        #self.dbcon.commit()
    
    
    def add_comments_history(self, comments_history):
        cursor = self.dbcon.cursor()
        query = "INSERT INTO fb_comment_history (comment_id, fb_comment_id, company_id, download_timestamp, likes_count) " \
                "VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(query, comments_history)
        cursor.close()
        #self.dbcon.commit()
    

    def add_feed_item(self, item_data):
        cursor = self.dbcon.cursor()
        query = ("INSERT INTO fb_feed_item (fb_id, company_id, created_timestamp, text,"
                 "init_likes_count, downloaded_timestamp, shares_count, comments_count, object_type, status_type,"
                 "from_name, from_id, story, link, mentioned_profiles, message_tags, place)"
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(query, item_data)
        return cursor.lastrowid


    def update_last_download(self, company_id, last_timestamp):
        cursor = self.dbcon.cursor()
        query = "UPDATE last_download SET fb_post_timestamp = %s WHERE company_id = %s"
        cursor.execute(query, (last_timestamp, company_id))
        # The last statement in the whole transaction - commit changes.
        self.dbcon.commit()
        cursor.close()

    def update_last_download_feed(self, company_id, last_timestamp):
        cursor = self.dbcon.cursor()
        query = "UPDATE last_download SET fb_feed_timestamp = %s WHERE company_id = %s"
        cursor.execute(query, (last_timestamp, company_id))
        # The last statement in the whole transaction - commit changes.
        self.dbcon.commit()
        cursor.close()
        