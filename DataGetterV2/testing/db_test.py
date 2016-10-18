#kkk!/usr/bin/python

import mysql.connector
import datetime

# Create connection
config = {
                'user': 'root',
                'password': 'autobus',
                'host': '127.0.0.1',
                'database': 'fin_analyzer_v2',
                'charset': 'utf8mb4',
                'collation': 'utf8mb4_general_ci'
        }
dbcon = mysql.connector.connect(**config)

# basic test
cursor = dbcon.cursor(dictionary=True)
cursor.execute('SELECT * FROM company WHERE id = 1')
print cursor.fetchone()['name']     # 3M Company

# unicode test
cursor.execute('SELECT * FROM test WHERE id=1')
print cursor.fetchone()['text']     # smajlik

# test
cursor.execute('SELECT id FROM company WHERE id = 115 ORDER BY id ASC')
for row in cursor:
    pass#print row['id']

cursor.execute("UPDATE test SET text = %s", ['\xF0\x9F\x98\x95'])

cursor.execute("UPDATE test SET timestamp = %s", [datetime.datetime.now()])

dbcon.commit()


query = 'SELECT id, url FROM article WHERE company_id = %s AND (published_date > DATE_SUB(NOW(), INTERVAL %s DAY))'
cursor.execute(query, (4, 14))
print cursor.fetchall()
