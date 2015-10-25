import json

# test for reading from created files


tfile = open('../data/twitter/mentions/amazon.tweets')
for line in tfile.readlines():
    print line,
    data = json.loads(line.rstrip())
    print "=="+data['s']['te']
    #break