import json
from collections import OrderedDict
import datetime

import mysql.connector

from classes.MyMailer import MyMailer


####
# When to run: every Friday at 22:00
####

# Create DB connection
config = json.load(open('../configs/databases.json'))['dev']
dbcon = mysql.connector.connect(**config)

# Set interval
days_ago = 7

####
# Get number of documents: articles, article comments, fb posts, fb feed items, fb commments, tweets
####
cursor = dbcon.cursor()
dl_stats = OrderedDict()

cursor.execute('SELECT COUNT(*) FROM article '
               'WHERE published_date >= DATE_SUB(NOW(), INTERVAL %s DAY)', [days_ago])
dl_stats['yahoo articles'] = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM article_comment '
               'WHERE created_datetime >= DATE_SUB(NOW(), INTERVAL %s DAY)', [days_ago])
dl_stats['yahoo comments'] = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM fb_post '
               'WHERE FROM_UNIXTIME(created_timestamp) >= DATE_SUB(NOW(), INTERVAL %s DAY)', [days_ago])
dl_stats['facebook posts'] = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM fb_comment '
               'WHERE FROM_UNIXTIME(created_timestamp) >= DATE_SUB(NOW(), INTERVAL %s DAY)', [days_ago])
dl_stats['facebook comments'] = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM fb_feed '
               'WHERE FROM_UNIXTIME(created_timestamp) >= DATE_SUB(NOW(), INTERVAL %s DAY)', [days_ago])
dl_stats['facebook feed items'] = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM tw_status '
               'WHERE created_at >= DATE_SUB(NOW(), INTERVAL %s DAY)', [days_ago])
dl_stats['tweets'] = cursor.fetchone()[0]

####
# Get script executions stats
####
cursor = dbcon.cursor(dictionary=True)
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
