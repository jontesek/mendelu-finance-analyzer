import json
from bs4 import BeautifulSoup

html = open('../test_data/ya2.htm').read()

# Create a main parse object
soup = BeautifulSoup(html, "html5lib")

# Find the script tag
script_content = soup.find('body').find('script')

lines = script_content.text.split('\n')

a_json_str = lines[-3][16:-1]

a_json = json.loads(a_json_str)

a_data = a_json['context']['dispatcher']['stores']['ContentStore']['uuidMap'].values()[0]

for (key, value) in  a_data.iteritems():
    print(">>>%s: %s") % (key, value)

quit()
#print a_data['body']

a_text = ''
for item in a_data['body']:
    if item['type'] == 'text':
        i_soup = BeautifulSoup(item['content'], "lxml")
        a_text += '<p>%s</p>' % i_soup.text

# Remove all extra whitespace (single space remains).
a_text = ' '.join(a_text.strip().split())

print a_text

