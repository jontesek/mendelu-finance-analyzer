
from bs4 import BeautifulSoup

html = open('../test_data/inplay_article.htm').read()

# Create a main parse object
soup = BeautifulSoup(html, "lxml")
# DIV - main content
content = soup.find('section', id='mediacontentstory')

a_content = soup.find('div', itemtype='http://schema.org/Article')

print soup
