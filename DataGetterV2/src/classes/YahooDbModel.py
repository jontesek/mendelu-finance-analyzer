from DbModel import DbModel



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
    
    def add_article(self, article, company_id, url, server_id):
        cursor = self.dbcon.cursor()
        # Insert article
        query = "INSERT INTO article (company_id, published_date, title, text, url, server_id) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (company_id, article['datetime'], article['title'], article['text'], url, server_id)
        cursor.execute(query, data)
        # Return inserted ID for history.
        return cursor.lastrowid

    
    def add_article_history(self, article_id, fb_shares, tw_shares):
        cursor = self.dbcon.cursor()
        query = "INSERT INTO article_history (article_id, download_timestamp, fb_shares, tw_shares) VALUES (%s, UNIX_TIMESTAMP(), %s, %s)"
        cursor.execute(query, (article_id, fb_shares, tw_shares))
        cursor.close()
        
    
    def update_last_download(self, company_id, newest_saved_date):
        cursor = self.dbcon.cursor()
        query = "UPDATE last_download SET article_newest_saved = %s WHERE company_id=%s"           
        cursor.execute(query, (newest_saved_date, company_id)) 
        # commit add_article, add_article_history inserts, this update
        self.dbcon.commit()
        cursor.close()

    
    def add_articles_history(self, articles_history):
        cursor = self.dbcon.cursor()
        query = "INSERT INTO article_history (article_id, download_timestamp, fb_shares, tw_shares) VALUES (%s, %s, %s, %s)"
        cursor.executemany(query, articles_history)
        self.dbcon.commit()
        cursor.close()
