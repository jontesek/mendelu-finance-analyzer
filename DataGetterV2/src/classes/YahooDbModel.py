from DbModel import DbModel

import json



class YahooDbModel(DbModel):
    '''
    classdocs
    '''


    def __init__(self):
        super(YahooDbModel, self).__init__()       # creates "dbcon" variable
        
    
    #### READ methods
    
    def get_companies(self):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id, ticker, article_newest_saved FROM company JOIN last_download ON id=company_id " \
                "WHERE ticker IS NOT NULL ORDER BY id ASC"
        cursor.execute(query)
        return cursor.fetchall()
    
    
    def get_companies_for_update(self):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id, ticker FROM company ORDER BY id ASC"
        cursor.execute(query)
        return cursor.fetchall()
    
    
    def get_articles_since(self, days, company_id, only_yahoo=False):
        cursor = self.dbcon.cursor(dictionary=True)
        query = ('SELECT id, company_id, published_date, url, yahoo_uuid FROM article '
                 'WHERE company_id = %s AND (published_date >= DATE_SUB(NOW(), INTERVAL %s DAY)) ')
        query += 'AND yahoo_uuid IS NOT NULL ' if only_yahoo else ''
        query += 'ORDER BY id ASC'
        cursor.execute(query, (company_id, days))
        return cursor.fetchall()


    def get_articles_in_interval(self, company_id, days_ago_from, days_ago_to, only_yahoo=False):
        cursor = self.dbcon.cursor(dictionary=True)
        query = ('SELECT id, company_id, published_date, url, yahoo_uuid FROM article '
                 'WHERE company_id = %s AND '
                 'published_date BETWEEN DATE_SUB(NOW(), INTERVAL %s DAY) AND DATE_SUB(NOW(), INTERVAL %s DAY) ')
        query += 'AND yahoo_uuid IS NOT NULL ' if only_yahoo else ''
        query += 'ORDER BY id ASC'
        cursor.execute(query, (company_id, days_ago_from, days_ago_to))
        return cursor.fetchall()


    def get_server_id(self, s_name, is_native):
        # Select ID of the server name
        cursor = self.dbcon.cursor()
        query = "SELECT id FROM article_server WHERE name = %s"
        cursor.execute(query, [s_name])
        # Is there any result?
        result = cursor.fetchone()
        # YES - return ID.
        if result:
            return result[0]
        # NO - insert server into DB.
        is_native = 1 if is_native else 0
        query = 'INSERT INTO article_server (name, native_yahoo) VALUES (%s, %s)'
        cursor.execute(query, (s_name, is_native))
        # Return new ID.
        return cursor.lastrowid


    def get_comments_for_article(self, article_id):
        cursor = self.dbcon.cursor()
        query = 'SELECT id, yahoo_id FROM article_comment WHERE article_id = %s'
        cursor.execute(query, [article_id])
        return cursor.fetchall()


    #### WRITE methods
    
    def add_article(self, article, company_id, server_id, downloaded_ts):
        cursor = self.dbcon.cursor()

        query = ("INSERT INTO article (company_id, server_id, published_date, url, title, text, summary, off_network, "
                 "doc_type, init_comment_count, yahoo_uuid, init_fb_shares_count, init_tw_shares_count, "
                 "author_name, author_title, j_tags, j_entities, downloaded_timestamp, created_timestamp_ms, "
                 "article_body_data, paragraph_count, word_count) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                 )

        j_tags = json.dumps(article['j_tags']) if article['j_tags'] else None
        j_entities = json.dumps(article['j_entities']) if article['j_entities'] else None

        data = (company_id, server_id, article['published_date'], article['url'], article['title'], article['text'],
                article['summary'], article['off_network'], article['doc_type'],
                article['comment_count'], article['yahoo_uuid'], article['fb_shares'], article['tw_shares'],
                article['author_name'], article['author_title'], j_tags, j_entities,
                downloaded_ts, article['created_timestamp'],
                article['article_body_data'], article['paragraph_count'], article['word_count'],
                )

        cursor.execute(query, data)

        return cursor.lastrowid

    
    def add_article_history(self, article_id, download_ts, fb_shares, tw_shares, yahoo_comments):
        cursor = self.dbcon.cursor()
        query = ("INSERT INTO article_history (article_id, downloaded_timestamp, fb_shares, tw_shares, yahoo_comments) "
                 "VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(query, (article_id, download_ts, fb_shares, tw_shares, yahoo_comments))
        cursor.close()
        
    
    def update_last_download(self, company_id):
        # Commit: add_article, add_article_history
        self.dbcon.commit()
        # Select the newest article in DB.
        cursor = self.dbcon.cursor()
        query = "SELECT MAX(published_date) FROM article WHERE company_id = %s"
        cursor.execute(query, [company_id])
        newest_saved_date = cursor.fetchone()[0] or '1900-01-01 00:00:01'
        # Update!
        query = "UPDATE last_download SET article_newest_saved = %s WHERE company_id=%s"           
        cursor.execute(query, (newest_saved_date, company_id))
        self.dbcon.commit()
        cursor.close()

    
    def add_articles_history(self, articles_history):
        cursor = self.dbcon.cursor()
        query = ("INSERT INTO article_history (article_id, downloaded_timestamp, fb_shares, tw_shares, yahoo_comments) "
                 "VALUES (%s, %s, %s, %s, %s)")
        cursor.executemany(query, articles_history)
        self.dbcon.commit()
        cursor.close()


    def add_comment(self, data):
        cursor = self.dbcon.cursor()
        query = ("INSERT INTO article_comment (article_id, company_id, created_datetime, yahoo_id, text, "
                 "reply_count, down_count, up_count, creator_id, user_profile_name, "
                 "downloaded_timestamp, created_timestamp_ms, paragraph_count, word_count) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(query, data)
        return cursor.lastrowid


    def add_comments_history(self, comments_history):
        cursor = self.dbcon.cursor()
        query = ("INSERT INTO article_comment_history (comment_id, article_id, company_id, yahoo_id, "
                 "reply_count, down_count, up_count, downloaded_timestamp) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.executemany(query, comments_history)
        self.dbcon.commit()
        cursor.close()
