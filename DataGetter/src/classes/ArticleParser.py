import datetime
from bs4 import BeautifulSoup

from exceptions.ParsingNotImplementedException import ParsingNotImplementedException


class ArticleParser(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
         
        
    
    def native_yahoo(self, html):
        """Parse a native yahoo finance article."""
        # Create main parse object
        soup = BeautifulSoup(html, "lxml")
        # DIV - main content
        content = soup.find('section', id='mediacontentstory')
        # Title
        title = content.find('h1', class_ = 'headline').text.strip()
        # Article date
        credit = content.find('div', class_ = 'credit')
        date_string = credit.find('abbr').text.strip()
        try: 
            # Old article - get article date from page.
            published_datetime = datetime.datetime.strptime(date_string, '%B %d, %Y %I:%M %p')
        except ValueError:
            # Recent article - should not be here, because we skip new articles.
            raise ParsingNotImplementedException('cannot parse recent article time')
        # get Text
        a_content = content.find('div', class_ = 'mw_release')
        if not a_content:
            a_content = content.find('div', itemtype = 'http://schema.org/Article')
            if not a_content:
                #a_content = '1_not_found'     # text not found
                raise Exception('Content DIV of the article was not found. title: '+title)
        # parse Text
        text = self.__yahoo_parse_text(a_content)
        # result
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
        # result
        return text
        
        