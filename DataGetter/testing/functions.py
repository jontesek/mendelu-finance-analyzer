
# Write all page posts.

print post['id'],
if 'story' in post: 
    print post['story']
else:
    print post['message']