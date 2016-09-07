from bs4 import BeautifulSoup

import json


class ArticleParser(object):
    """
    Parsing HTML articles from Yahoo Finance.
    """

    def native_yahoo(self, html, parse_datetime=False):
        """Parse a native yahoo finance article."""
        # Create a main parse object
        soup = BeautifulSoup(html, "html5lib")
        # Find the script tag
        script_content = soup.find('body').find('script')
        # Get JSON data
        lines = script_content.text.split('\n')
        a_json_str = lines[-3][16:-1]
        a_json = json.loads(a_json_str)
        a_data = a_json['context']['dispatcher']['stores']['ContentStore']['uuidMap'].values()[0]
        # Parse Text
        text = self.__yahoo_parse_text(a_data)
        # Result
        return {
            'text': text,
            'j_entities': a_data['entities'],
            'j_tags': a_data['tags'],
            'type': a_data['type']
        }

    def __yahoo_parse_text(self, a_data):
        """Edit article text to suitable format."""
        a_text = ''
        for item in a_data['body']:
            if item['type'] == 'text':
                i_soup = BeautifulSoup(item['content'], "lxml")
                a_text += '<p>%s</p>' % i_soup.text
        # Remove all extra whitespace (single space remains).
        a_text = ' '.join(a_text.strip().split())
        # Result
        return a_text
