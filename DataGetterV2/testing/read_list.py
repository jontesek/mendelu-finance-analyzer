import json

#sample_page = '../test_data/ticker_not_found.htm'
sample_page = '../test_data/mmm_list.html'

sample_file = open(sample_page, 'r')

lines = sample_file.readlines()

# Check if it's not 404 error.
header_line = lines[0]
if '<title></title>' in header_line:
    exit('404 error')

# Find JSON data
app_data = None
for s_line in lines:
    if s_line.lstrip().startswith('root.App.main'):
        app_data = s_line[16:-2]
        break

if not app_data:
    exit('JSON data not found.')


# with open('../test_data/yahoo.json', 'w') as json_file:
#     json_file.write(app_data)

json_data = json.loads(app_data)

#articles = json_data['context']['dispatcher']['stores']['StreamStore']['streams']['YFINANCE:AMD.mega']['data']['stream_items']

page_name = json_data['context']['dispatcher']['stores']['StreamStore']['pageCategory']
page_field = '%s.mega' % page_name

articles = json_data['context']['dispatcher']['stores']['StreamStore']['streams'][page_field]['data']['stream_items']

article = articles[1]

for key, value in article.iteritems():
    print('>%s: %s') % (key, value)

exit()
# PROCESS ONE ARTICLE
def process_article(article):
    if article['type'] == 'ad':
        return('add')
    # musi se rovnat "article"

    a_data = {
        'publisher': article['publisher'],
        'title': article['title'],
        'url': article['url'],
        'summary': article['summary'],
        'pubtime': article['pubtime'],
        'comments_count': 0,
    }

    if 'commentCount' in article:
        a_data['comments_count'] = article['commentCount']

    # Nelze stahnout plny text, pujde se na preview.
    if article['off_network']:
        return('off')

    print a_data

#
article = articles[0]
print process_article(article)
