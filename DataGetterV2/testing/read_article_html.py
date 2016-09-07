
from bs4 import BeautifulSoup

html = open('../test_data/yahoo_article.htm').read()

# Create a main parse object
soup = BeautifulSoup(html, "lxml")
# DIV - main content
content = soup.find('div', id='Main')

paragraphs = content.find_all('p')
a_text = ''

for i, par in enumerate(paragraphs):
    print('%d %s') % (i, par.text)
    a_text += '<p>%s</p>' % par.getText(separator=' ')
# Remove all extra whitespace (single space remains).
a_text = ' '.join(a_text.strip().split())

print a_text
