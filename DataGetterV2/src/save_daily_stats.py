from collections import OrderedDict
import datetime
import time
import os.path

from classes.DbStats import DbStats

os.chdir(os.path.dirname(os.path.abspath(__file__)))

####
# When to run: every day at 23:00
####

dbstats = DbStats()
days_ago = 1

# Get data
dl_stats = OrderedDict()
dl_stats['yahoo_articles'] = dbstats.count_yahoo_articles(days_ago)
dl_stats['yahoo_comments'] = dbstats.count_yahoo_comments(days_ago)
dl_stats['facebook_posts'] = dbstats.count_facebook_posts(days_ago)
dl_stats['facebook_comments'] = dbstats.count_facebook_comments(days_ago)
dl_stats['facebook_feed_items'] = dbstats.count_facebook_feed_items(days_ago)
dl_stats['tweets'] = dbstats.count_tweets(days_ago)

# Insert data into DB
cursor = dbstats.dbcon.cursor()
prepared_sql = ("INSERT INTO stats_download (created_timestamp, date_created, {columns}) "
                "VALUES ({ts}, '{day}', {values})"
                .format(
                    ts=int(time.time()),
                    day=str(datetime.date.today()),
                    columns=', '.join([str(x) for x in dl_stats.keys()]),
                    values=', '.join([str(x) for x in dl_stats.values()])
                ))
cursor.execute(prepared_sql)
dbstats.dbcon.commit()

print cursor.statement
