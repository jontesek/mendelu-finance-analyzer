from bs4 import BeautifulSoup

import json


class ArticleParser(object):
    """
    Parsing HTML articles from Yahoo Finance.
    """

    def parse_native_yahoo(self, html):
        """Parse a native yahoo finance article."""
        json_data = self._get_json_data(html)
        try:
            article_data = json_data['context']['dispatcher']['stores']['ContentStore']['uuidMap'].values()[0]
        except TypeError, e:
            print str(e)
            return False
        # Parse Text
        text = self.__yahoo_parse_text(article_data)
        author_name, author_title = self._get_author_from_json(article_data)
        # Result
        return {
            'text': text,
            'j_entities': article_data['entities'],
            'j_tags': article_data['tags'] if article_data['tags'] else None,
            'doc_type': article_data['type'],
            'author_name': author_name,
            'author_title': author_title,
        }

    def parse_yahoo_preview(self, html):
        json_data = self._get_json_data(html)
        try:
            page_data = json_data['context']['dispatcher']['stores']['PageStore']['pageData']
        except TypeError, e:
            print str(e)
            return False
        author_name, author_title = self._get_author_from_json(page_data)
        return {
            'text': page_data['description'],
            'j_entities': page_data['entities'],
            'j_tags': None,
            'doc_type': 'a_preview',
            'author_name': author_name,
            'author_title': author_title,
        }

    # PRIVATE METHODS

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

    def _get_json_data(self, text_file):
        app_data = None
        for line in text_file:
            if line.lstrip().startswith('root.App.main'):
                app_data = line[16:-2]
                break
        if app_data:
            return json.loads(app_data)
        else:
            return False

    def _get_author_from_json(self, json_dict):
        author_name, author_title = None, None
        if 'author' in json_dict and json_dict['author']:
            if 'name' in json_dict['author']:
                author_name = json_dict['author']['name']
            else:
                author_name = json_dict['author']
            if 'title' in json_dict['author']:
                author_title = json_dict['author']['title']

        return author_name, author_title

