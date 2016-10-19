import json
from collections import OrderedDict
import datetime

from classes.MyMailer import MyMailer
from classes.DbStats import DbStats

####
# When to run: every Friday at 23:00
####

dbstats = DbStats()
days_ago = 7

####
# Get number of documents: articles, article comments, fb posts, fb feed items, fb commments, tweets
####
dl_stats = OrderedDict()

dl_stats['yahoo articles'] = dbstats.count_yahoo_articles(days_ago)

dl_stats['yahoo comments'] = dbstats.count_yahoo_comments(days_ago)

dl_stats['facebook posts'] = dbstats.count_facebook_posts(days_ago)

dl_stats['facebook comments'] = dbstats.count_facebook_comments(days_ago)

dl_stats['facebook feed items'] = dbstats.count_facebook_feed_items(days_ago)

dl_stats['tweets'] = dbstats.count_tweets(days_ago)

####
# Get script executions stats
####
cursor = dbstats.dbcon.cursor(dictionary=True)
cursor.execute('SELECT COUNT(*) as run_count, script_name, SEC_TO_TIME(AVG(TIME_TO_SEC(duration))) as avg_duration, '
               'SUM(TIME_TO_SEC(duration)) as total_duration '
               'FROM log_exec WHERE end_time >= DATE_SUB(NOW(), INTERVAL %s DAY)'
               'GROUP BY script_name ORDER BY script_name', [days_ago])
run_stats = cursor.fetchall()

####
# Create the message
####
today_dt = datetime.date.today()
first_dt = today_dt - datetime.timedelta(days=days_ago)
today_str = today_dt.strftime('%d.%m.%Y')
first_str = first_dt.strftime('%d.%m.%Y')

msg = 'Dear user,\nplease see summary statistics for last week ({0} - {1}).'.format(first_str, today_str)

msg += '\n\n===Number of downloaded documents===\n'
for name, count in dl_stats.iteritems():
    msg += '- {0}: {1}\n'.format(name.capitalize(), count)
msg += '\nTotal number of documents: {0}'.format(sum(dl_stats.values()))

msg += '\n\n===Scripts executions===\n'
for script in run_stats:
    msg += ('- {0}: {1}x, avg {2}\n'
            .format(script['script_name'], script['run_count'], script['avg_duration'])
            )
msg += ('\nTotal script runs: {0}x, total duration: {1} hours'
        .format(sum([x['run_count'] for x in run_stats]),
                round(sum([float(x['total_duration']) for x in run_stats]) / 3600.0), 2)
        )

msg += '\n\n\nFinance DataGetter from sosna.mendelu.cz'

####
# Send the email
####
subject = 'Finance DataGetter -- weekly summary: {0} - {1}'.format(first_str, today_str)
email_from = 'apps.noreply@petrovsky.cz'
emails_to = ['jond@post.cz']

MyMailer.send_email(email_from, emails_to, subject, msg)

print msg
