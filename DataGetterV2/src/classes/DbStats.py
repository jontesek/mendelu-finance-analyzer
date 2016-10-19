from DbModel import DbConnection


class DbStats:

    def __init__(self):
        self.dbcon = DbConnection.get_con()

    def count_yahoo_articles(self, days_ago):
        cursor = self.dbcon.cursor()
        cursor.execute('SELECT COUNT(*) FROM article '
                       'WHERE published_date >= DATE_SUB(NOW(), INTERVAL %s DAY)', [days_ago])
        return cursor.fetchone()[0]

    def count_yahoo_comments(self, days_ago):
        cursor = self.dbcon.cursor()
        cursor.execute('SELECT COUNT(*) FROM article_comment '
                       'WHERE created_datetime >= DATE_SUB(NOW(), INTERVAL %s DAY)', [days_ago])
        return cursor.fetchone()[0]

    def count_facebook_posts(self, days_ago):
        cursor = self.dbcon.cursor()
        cursor.execute('SELECT COUNT(*) FROM fb_post '
                       'WHERE FROM_UNIXTIME(created_timestamp) >= DATE_SUB(NOW(), INTERVAL %s DAY)', [days_ago])
        return cursor.fetchone()[0]

    def count_facebook_comments(self, days_ago):
        cursor = self.dbcon.cursor()
        cursor.execute('SELECT COUNT(*) FROM fb_comment '
                       'WHERE FROM_UNIXTIME(created_timestamp) >= DATE_SUB(NOW(), INTERVAL %s DAY)', [days_ago])
        return cursor.fetchone()[0]

    def count_facebook_feed_items(self, days_ago):
        cursor = self.dbcon.cursor()
        cursor.execute('SELECT COUNT(*) FROM fb_feed_item '
                       'WHERE FROM_UNIXTIME(created_timestamp) >= DATE_SUB(NOW(), INTERVAL %s DAY)', [days_ago])
        return cursor.fetchone()[0]

    def count_tweets(self, days_ago):
        cursor = self.dbcon.cursor()
        cursor.execute('SELECT COUNT(*) FROM tw_status '
                       'WHERE created_at >= DATE_SUB(NOW(), INTERVAL %s DAY)', [days_ago])
        return cursor.fetchone()[0]
