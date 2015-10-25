# Get page posts
posts = graph.get('22707976849/posts')
jsdump = json.dumps(posts)
text_file = open("fb_inputs/intel_posts.json", "w")
text_file.write(jsdump)
text_file.close()
