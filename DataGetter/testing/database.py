#kkk!/usr/bin/python

import mysql.connector
import datetime

# Create connection
config = {
                'user': 'root',
                'password': 'auto',
                'host': '127.0.0.1',
                'database': 'fin_analyzer',
                'charset': 'utf8mb4',
                'collation': 'utf8mb4_general_ci'
        }
dbcon = mysql.connector.connect(**config)

cursor = dbcon.cursor()
########
post = {'id': 2}
comments_history = []
company_id = 4
current_timestamp = 14878
# Get comments for post
query = "SELECT id, fb_id FROM fb_comment WHERE post_id = 2"
cursor.execute(query, (post['id']))
db_comments = cursor.fetchall()
# Create dictionary from comments
db_com_dict = {fb_id: db_id for (db_id, fb_id) in db_comments}
# Process FB comments
fb_comments = [
               ({'id': '10155590261920374_10155618060855374', 'created_time': 123, 'message': 'Hello', 'like_count': 3}),
               ({'id': '10155590261920374_muj1', 'created_time': 147, 'message': 'Good day', 'like_count': 5})
]
# Insert history for actual comments
for fb_com in fb_comments:
    # Check if comment ID is already in DB.
    if fb_com['id'] in db_com_dict:
        # YES - only add item to history.
        comments_history.append([db_com_dict[fb_com['id']], fb_com['id'], company_id, current_timestamp, int(fb_com['like_count'])])
    else:
        # NO - insert comment into DB, get ID and add item to history.
        query = "INSERT INTO fb_comment (fb_id, post_id, company_id, created_timestamp, text, fb_author_id) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (fb_com['id'], post['id'], company_id, fb_com['created_time'], fb_com['message'], 'author'))
        com_db_id = cursor.lastrowid   
        comments_history.append([com_db_id, fb_com['id'], company_id, current_timestamp, int(fb_com['like_count'])])

print comments_history

        
    