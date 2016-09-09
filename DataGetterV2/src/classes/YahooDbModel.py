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
        query = "SELECT id, ticker, article_newest_saved FROM company JOIN last_download ON id=company_id WHERE ticker IS NOT NULL ORDER BY id ASC"
        cursor.execute(query)
        return cursor.fetchall()
    
    
    def get_companies_update(self):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id FROM company ORDER BY id ASC"
        cursor.execute(query)
        return cursor.fetchall()
    
    
    def get_articles_since(self, days, company_id):
        cursor = self.dbcon.cursor(dictionary=True)
        query = 'SELECT id, url FROM article WHERE company_id = %s AND (published_date >= DATE_SUB(NOW(), INTERVAL %s DAY))'
        cursor.execute(query, (company_id, days))
        return cursor
    
    
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


    #### WRITE methods
    
    def add_article(self, article, company_id, server_id):
        cursor = self.dbcon.cursor()
        # Insert article
        query = "INSERT INTO article (company_id, server_id, published_date, title, text, url, summary, off_network, " \
                "comment_count, doc_type, init_fb_shares_count, init_tw_shares_count, author_name, author_title, j_tags, j_entities) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        j_tags = json.dumps(article['j_tags'])
        if j_tags == 'null':
            j_tags = None
        data = (company_id, server_id, article['published_date'], article['title'], article['text'], article['url'], article['summary'], article['off_network'],
                article['comment_count'], article['doc_type'], article['fb_shares'], article['tw_shares'],
                article['author_name'], article['author_title'], j_tags, json.dumps(article['j_entities']))
        cursor.execute(query, data)
        # Return inserted ID (for history).
        return cursor.lastrowid

    
    def add_article_history(self, article_id, fb_shares, tw_shares):
        cursor = self.dbcon.cursor()
        query = "INSERT INTO article_history (article_id, download_timestamp, fb_shares, tw_shares) VALUES (%s, UNIX_TIMESTAMP(), %s, %s)"
        cursor.execute(query, (article_id, fb_shares, tw_shares))
        cursor.close()
        
    
    def update_last_download(self, company_id):
        # Commit: add_article, add_article_history
        self.dbcon.commit()
        # Select the newest article in DB.
        cursor = self.dbcon.cursor()
        query = "SELECT MAX(published_date) FROM article WHERE company_id = %s"
        cursor.execute(query, [company_id])
        newest_saved_date = cursor.fetchone()[0]
        # Update!
        query = "UPDATE last_download SET article_newest_saved = %s WHERE company_id=%s"           
        cursor.execute(query, (newest_saved_date, company_id))
        self.dbcon.commit()
        cursor.close()

    
    def add_articles_history(self, articles_history):
        cursor = self.dbcon.cursor()
        query = "INSERT INTO article_history (article_id, download_timestamp, fb_shares, tw_shares) VALUES (%s, %s, %s, %s)"
        cursor.executemany(query, articles_history)
        self.dbcon.commit()
        cursor.close()
