import datetime
from bs4 import BeautifulSoup

from exceptions.ParsingNotImplementedException import ParsingNotImplementedException


class ArticleParser(object):
    """
    Parsing HTML articles from Yahoo Finance.
    """

    def native_yahoo(self, html, parse_datetime=False):
        """Parse a native yahoo finance article."""
        # Create a main parse object
        soup = BeautifulSoup(html, "lxml")
        # DIV - main content
        content = soup.find('section', id='mediacontentstory')
        # Title
        title = content.find('h1', class_='headline').text.strip()
        # Article date.
        if parse_datetime:
            credit = content.find('div', class_='credit')
            date_string = credit.find('abbr').text.strip()
            try:
                # Old article - get article date from page.
                published_datetime = datetime.datetime.strptime(date_string, '%B %d, %Y %I:%M %p')
            except ValueError:
                # Recent article - should not be here, because we skip new articles.
                published_datetime = False
        else:
            published_datetime = False
        # Get article Text
        a_content = content.find('div', class_='mw_release')
        if not a_content:
            a_content = content.find('div', itemtype='http://schema.org/Article')
            # Unfortunately, sometimes this does not work, even if the tag is present. Probably JS rendering...
            # See http://finance.yahoo.com/news/inplay-briefing-com-055139997.html
            if not a_content:
                raise ParsingNotImplementedException('Content DIV of the article was not found. Title: '+title)
        # Parse Text
        text = self.__yahoo_parse_text(a_content)
        # Result
        return {'title': title, 'datetime': published_datetime, 'text': text}


    def __yahoo_parse_text(self, content):
        """Edit article text to suitable format."""
        text = ''
        # Process all paragraphs.
        paragraphs = content.find_all('p')
        for par in paragraphs:
            text += '<p>' + par.getText(separator=' ') + '</p>'
        # Remove all extra whitespace (single space remains).
        text = ' '.join(text.strip().split())
        # Result
        return text
        