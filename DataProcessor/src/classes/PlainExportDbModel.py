import time

from DbModel import DbModel

class PlainExportDbModel(DbModel):

    #### READ documents

    def get_articles_for_company(self, company_id, from_date):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id, title, text, published_date FROM article WHERE company_id = %s AND published_date >= %s " \
                "ORDER BY published_date ASC"
        cursor.execute(query, [company_id, from_date])
        return cursor

    def get_fb_posts_for_company(self, company_id, from_date):
        cursor = self.dbcon.cursor(dictionary=True)
        from_date_timestamp = self._from_date_to_timestamp(from_date)
        query = "SELECT id, created_timestamp, text FROM fb_post WHERE company_id = %s AND created_timestamp >= %s " \
                "ORDER BY created_timestamp ASC"
        cursor.execute(query, [company_id, from_date_timestamp])
        return cursor

    def get_fb_comments_for_company(self, company_id, from_date):
        cursor = self.dbcon.cursor(dictionary=True)
        from_date_timestamp = self._from_date_to_timestamp(from_date)
        query = "SELECT id, created_timestamp, text FROM fb_comment WHERE company_id = %s AND created_timestamp >= %s " \
                "ORDER BY created_timestamp ASC"
        cursor.execute(query, [company_id, from_date_timestamp])
        return cursor

    def get_tweets_for_company(self, company_id, from_date):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT created_at, text FROM tw_status WHERE company_id = %s AND created_at >= %s " \
                "ORDER BY created_at ASC"
        cursor.execute(query, [company_id, from_date])
        return cursor

    def get_stock_prices(self, company_id, from_date):
        cursor = self.dbcon.cursor()
        query = "SELECT DATE_FORMAT(date, '%d.%m.%Y'), close FROM stock_price WHERE company_id = %s AND date >= %s"
        cursor.execute(query, (company_id, from_date))
        return cursor.fetchall()


    #### HELPERS

    def _from_date_to_timestamp(self, input_date):
        return long(time.mktime(input_date.timetuple()))