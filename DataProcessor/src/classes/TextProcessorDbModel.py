import time
from DbModel import DbModel


class TextProcessorDbModel(DbModel):

    #### READ documents

    def get_articles_for_company(self, company_id):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id, title, text, published_date FROM article WHERE company_id = %s"
        cursor.execute(query, [company_id])
        return cursor

    def get_fb_posts_for_company(self, company_id, from_date):
        cursor = self.dbcon.cursor(dictionary=True)
        from_date_timestamp = self._from_date_to_timestamp(from_date)
        query = "SELECT id, created_timestamp, text FROM fb_post WHERE company_id = %s AND created_timestamp >= %s"
        cursor.execute(query, [company_id, from_date_timestamp])
        return cursor

    def get_fb_comments_for_company(self, company_id):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id, created_timestamp, text, author_name FROM fb_comment WHERE company_id = %s"
        cursor.execute(query, [company_id])
        return cursor

    def get_fb_comments_for_post(self, post_id):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id, created_timestamp, text, author_name FROM fb_comment WHERE post_id = %s"
        cursor.execute(query, [post_id])
        return cursor

    def get_companies(self):
        cursor = self.dbcon.cursor(buffered=True)
        query = 'SELECT id FROM COMPANY ORDER BY id ASC'
        cursor.execute(query)
        return cursor

    #### READ stock prices

    def get_stock_prices(self, company_id, from_date):
        cursor = self.dbcon.cursor()
        query = 'SELECT date, close FROM stock_price WHERE company_id = %s AND date >= %s'
        cursor.execute(query, (company_id, from_date))
        return cursor.fetchall()

    #### HELPERS

    def _from_date_to_timestamp(self, input_date):
        return long(time.mktime(input_date.timetuple()))





