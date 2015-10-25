# Imports
import facepy
import json

# Get access token
token = facepy.utils.get_application_access_token('169550103254801', '2ec0d363d00345ef25e6a2e0a64a4d27')

# Create graph object
graph = facepy.GraphAPI(token)

# Get basic page info
#page = graph.get('22707976849')
#print coca['likes']

# Get page posts
#posts = graph.get('22707976849/posts')

jfile = open('fb_inputs/intel_posts.json')
posts = json.load(jfile);

for post in posts['data']:
    print post['id'],
    if 'story' in post: 
        print post['story']
    else:
        print post['message']
