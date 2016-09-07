import json
from bs4 import BeautifulSoup

html = open('../test_data/yahoo_preview.htm').read()

# Create a main parse object
soup = BeautifulSoup(html, "lxml")

# Find the desired tags
title = soup.find('head').find('title').text
description = soup.find('head').find('meta', attrs={'name': 'description'})['content']
url = soup.find('div', id='app').find('a', attrs={'class': 'read-more-button'})['href']

print url
