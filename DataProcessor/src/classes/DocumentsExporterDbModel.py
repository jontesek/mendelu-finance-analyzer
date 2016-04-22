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

    #### READ daily documents

    def get_daily_articles_for_company(self, company_id, for_date, docs_query_limit=1000):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id, title, text, published_date FROM article " \
                "WHERE DATE(published_date) == %s AND company_id = %s LIMIT %s"
        cursor.execute(query, [for_date, company_id, docs_query_limit])
        return cursor

    def get_daily_fb_posts_for_company(self, company_id, for_date, docs_query_limit=1000):
        cursor = self.dbcon.cursor(dictionary=True)
        from_timestamp = self._from_date_to_timestamp(for_date.replace(hours=0, minutes=0, seconds=0))
        to_timestamp = self._from_date_to_timestamp(for_date.replace(hours=23, minutes=59, seconds=59))
        query = "SELECT id, created_timestamp, text FROM fb_post " \
                "WHERE created_timestamp BETWEEN %s AND %s AND company_id = %s LIMIT %s"
        cursor.execute(query, [from_timestamp, to_timestamp, company_id, docs_query_limit])
        return cursor

    def get_daily_fb_comments_for_company(self, company_id, for_date, docs_query_limit=1000):
        """
        Get Facebook comments created on given day. Exclude duplicates - GROUP BY(text).
        :param company_id:
        :param for_date:
        :param docs_query_limit:
        :return:
        """
        cursor = self.dbcon.cursor(dictionary=True)
        from_timestamp = self._from_date_to_timestamp(for_date.replace(hours=0, minutes=0, seconds=0))
        to_timestamp = self._from_date_to_timestamp(for_date.replace(hours=23, minutes=59, seconds=59))
        query = "SELECT id, created_timestamp, text FROM fb_comment " \
                "WHERE created_timestamp BETWEEN %s AND %s AND company_id = %s " \
                "ORDER BY id ASC LIMIT %s"
        cursor.execute(query, [from_timestamp, to_timestamp, company_id, docs_query_limit])
        return cursor

    def get_daily_tweets_for_company(self, company_id, for_date, docs_query_limit=1000):
        """
        Get tweets created on given day. Exclude duplicates - GROUP BY(text).
        :param company_id:
        :param for_date:
        :param docs_query_limit:
        :return:
        """
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT SQL_CACHE created_at, text, retweet_count FROM tw_status " \
                "WHERE DATE(created_at) = %s AND company_id = %s " \
                "GROUP BY(text) ORDER BY retweet_count DESC LIMIT %s"
        cursor.execute(query, [for_date, company_id, docs_query_limit])
        #exit(cursor.statement)
        return cursor

    #### READ companies

    def get_companies(self):
        cursor = self.dbcon.cursor(buffered=True)
        query = 'SELECT id FROM COMPANY ORDER BY id ASC'
        cursor.execute(query)
        return cursor

    def get_selected_companies(self, companies_ids):
        cursor = self.dbcon.cursor(buffered=True)
        ids_string = ','.join(['%s'] * len(companies_ids))
        query = 'SELECT id FROM COMPANY WHERE id IN (%s) ORDER BY id ASC' % ids_string
        cursor.execute(query, tuple(companies_ids))
        return cursor.fetchall()

    def get_companies_by_source(self, source_type):
        # Choose a correct query.
        if source_type == 'facebook':
            query = 'SELECT id FROM COMPANY WHERE fb_page IS NOT NULL ORDER BY id ASC'
        elif source_type == 'twitter':
            query = 'SELECT id FROM COMPANY WHERE tw_name IS NOT NULL ORDER BY id ASC'
        elif source_type == 'yahoo':
            query = 'SELECT id FROM COMPANY WHERE ticker IS NOT NULL ORDER BY id ASC'
        else:
            raise ValueError('Unknown document source.')
        # Execute query.
        cursor = self.dbcon.cursor(buffered=True)
        cursor.execute(query)
        return cursor

    #### HELPERS

    def _from_date_to_timestamp(self, input_date):
        return long(time.mktime(input_date.timetuple()))









