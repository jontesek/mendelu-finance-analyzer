import json
from bs4 import BeautifulSoup

#### DOM approach

html = open('../test_data/yahoo_preview.htm').read()

# Create a main parse object.
soup = BeautifulSoup(html, "lxml")

# Find the desired tags.
title = soup.find('head').find('title').text
description = soup.find('head').find('meta', attrs={'name': 'description'})['content']
url = soup.find('div', id='app').find('a', attrs={'class': 'read-more-button'})['href']

#### STRING approach

sample_file = open('../test_data/yahoo_preview.htm')
lines = sample_file.readlines()

# Find JSON data
app_data = None
for s_line in lines:
    if s_line.lstrip().startswith('root.App.main'):
        app_data = s_line[16:-2]
        break

# Create dict
json_data = json.loads(app_data)

page_data = json_data['context']['dispatcher']['stores']['PageStore']['pageData']

for (key, value) in page_data.iteritems():
    print(">>>%s: %s") % (key, value)

print page_data['description']
print page_data['entities']
