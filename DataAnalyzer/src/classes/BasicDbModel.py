import datetime
import time


from FaCommon.DbModel import DbModel


class BasicDbModel(DbModel):

    #### READ documents

    def get_daily_articles(self, company_id, examined_date):
        cursor = self.dbcon.cursor(dictionary=True)
        start_time = examined_date
        end_time = examined_date + datetime.timedelta(days=1)
        query = "SELECT id, title, text FROM article WHERE company_id = %s AND published_date >= %s AND published_date < %s"
        cursor.execute(query, [company_id, start_time, end_time])
        return cursor

    def get_daily_fb_posts(self, company_id, examined_date):
        cursor = self.dbcon.cursor(dictionary=True)
        start_ts = self._from_date_to_timestamp(examined_date)
        end_ts = start_ts + 24*3600 - 1
        query = "SELECT id, text FROM fb_post WHERE company_id = %s AND created_timestamp BETWEEN %s AND %s"
        cursor.execute(query, [company_id, start_ts, end_ts])
        return cursor.fetchall()

    def get_daily_fb_comments(self, company_id, examined_date):
        cursor = self.dbcon.cursor(dictionary=True)
        start_ts = self._from_date_to_timestamp(examined_date)
        end_ts = start_ts + 24*3600 - 1
        query = "SELECT id, text FROM fb_comment WHERE company_id = %s AND created_timestamp BETWEEN %s AND %s"
        cursor.execute(query, [company_id, start_ts, end_ts])
        return cursor

    def get_fb_comments_for_post(self, post_id):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id, created_timestamp, text, author_name FROM fb_comment WHERE post_id = %s"
        cursor.execute(query, [post_id])
        return cursor

    def get_daily_tweets(self, company_id, examined_date):
        cursor = self.dbcon.cursor(dictionary=True)
        start_time = examined_date
        end_time = examined_date + datetime.timedelta(days=1)
        query = "SELECT tw_id, text FROM tw_status WHERE company_id = %s AND created_at >= %s AND created_at < %s"
        cursor.execute(query, [company_id, start_time, end_time])
        return cursor

    #### READ documents 2

    def get_articles(self, company_id, date_from, date_to):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id, title, text FROM article WHERE company_id = %s AND published_date BETWEEN %s AND %s"
        cursor.execute(query, [company_id, date_from, date_to])
        return cursor

    def get_fb_posts(self, company_id, date_from, date_to):
        cursor = self.dbcon.cursor(dictionary=True)
        start_ts = self._from_date_to_timestamp(date_from)
        end_ts = self._from_date_to_timestamp(date_to)
        query = "SELECT id, text FROM fb_post WHERE company_id = %s AND created_timestamp BETWEEN %s AND %s"
        cursor.execute(query, [company_id, start_ts, end_ts])
        return cursor

    def get_fb_comments(self, company_id, date_from, date_to):
        cursor = self.dbcon.cursor(dictionary=True)
        start_ts = self._from_date_to_timestamp(date_from)
        end_ts = self._from_date_to_timestamp(date_to)
        query = "SELECT id, text FROM fb_comment WHERE company_id = %s AND created_timestamp BETWEEN %s AND %s"
        cursor.execute(query, [company_id, start_ts, end_ts])
        return cursor

    def get_tweets(self, company_id, date_from, date_to):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT tw_id, text FROM tw_status WHERE company_id = %s AND created_at BETWEEN %s AND %s"
        cursor.execute(query, [company_id, date_from, date_to])
        return cursor


    #### READ other

    def get_companies(self):
        cursor = self.dbcon.cursor(dictionary=True)
        query = 'SELECT id FROM COMPANY ORDER BY id ASC'
        cursor.execute(query)
        return cursor.fetchall()

    def get_companies_order_by_total_documents(self, start_date, end_date):
        cursor = self.dbcon.cursor(dictionary=True)
        query = """
            SELECT company.id,
            (SELECT COUNT(*) FROM article WHERE company_id = company.id) +
            (SELECT COUNT(*) FROM fb_post WHERE company_id = company.id) +
            (SELECT COUNT(*) FROM fb_comment WHERE company_id = company.id) +
            (SELECT COUNT(*) FROM tw_status WHERE company_id = company.id)
            AS DocsCount
            FROM company
            ORDER BY DocsCount DESC
        """ 
        cursor.execute(query)
        return cursor.fetchall()

    #### HELPERS

    def _from_date_to_timestamp(self, input_date):
        return long(time.mktime(input_date.timetuple()))






