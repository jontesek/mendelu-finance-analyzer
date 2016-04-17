import time
from DbModel import DbModel


class DocumentsExporterDbModel(DbModel):

    #### READ documents

    def get_articles_for_company(self, company_id, from_date):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id, title, text, published_date FROM article WHERE company_id = %s AND published_date >= %s"
        cursor.execute(query, [company_id, from_date])
        return cursor

    def get_fb_posts_for_company(self, company_id, from_date):
        cursor = self.dbcon.cursor(dictionary=True)
        from_date_timestamp = self._from_date_to_timestamp(from_date)
        query = "SELECT id, created_timestamp, text FROM fb_post WHERE company_id = %s AND created_timestamp >= %s"
        cursor.execute(query, [company_id, from_date_timestamp])
        return cursor

    def get_fb_comments_for_company(self, company_id, from_date):
        cursor = self.dbcon.cursor(dictionary=True)
        from_date_timestamp = self._from_date_to_timestamp(from_date)
        query = "SELECT id, created_timestamp, text FROM fb_comment WHERE company_id = %s AND created_timestamp >= %s"
        cursor.execute(query, [company_id, from_date_timestamp])
        return cursor

    def get_tweets_for_company(self, company_id, from_date):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT created_at, text FROM tw_status WHERE company_id = %s AND created_at >= %s"
        cursor.execute(query, [company_id, from_date])
        return cursor

    #### READ random documents

    def get_random_articles(self, for_date, docs_per_day):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id, title, text, published_date FROM article " \
                "WHERE DATE(published_date) == %s LIMIT %s"
        cursor.execute(query, [for_date, docs_per_day])
        return cursor

    def get_random_fb_posts(self, for_date, docs_per_day):
        cursor = self.dbcon.cursor(dictionary=True)
        from_timestamp = self._from_date_to_timestamp(for_date.replace(hours=0, minutes=0, seconds=0))
        to_timestamp = self._from_date_to_timestamp(for_date.replace(hours=23, minutes=59, seconds=59))
        query = "SELECT id, created_timestamp, text FROM fb_post " \
                "WHERE company_id = %s AND created_timestamp BETWEEN %s AND %s LIMIT %s"
        cursor.execute(query, [from_timestamp, to_timestamp, docs_per_day])
        return cursor

    def get_random_fb_comments(self, for_date, docs_per_day):
        cursor = self.dbcon.cursor(dictionary=True)
        from_date_timestamp = self._from_date_to_timestamp(for_date)
        query = "SELECT id, created_timestamp, text FROM fb_comment " \
                "WHERE company_id = %s AND created_timestamp >= %s LIMIT %s"
        cursor.execute(query, [from_date_timestamp, docs_per_day])
        return cursor

    def get_random_tweets(self, for_date, docs_per_day):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT tw_id, created_at, text FROM tw_status " \
                "WHERE company_id = %s AND DATE(created_at) == %s LIMIT %s"
        cursor.execute(query, [for_date, docs_per_day])
        return cursor

    #### READ other

    def get_companies(self):
        cursor = self.dbcon.cursor(buffered=True)
        query = 'SELECT id FROM COMPANY ORDER BY id ASC'
        cursor.execute(query)
        return cursor

    #### HELPERS

    def _from_date_to_timestamp(self, input_date):
        return long(time.mktime(input_date.timetuple()))







