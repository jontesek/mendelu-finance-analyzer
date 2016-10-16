import json

from bs4 import BeautifulSoup

from my_exceptions import AppDataNotFoundRetryException


class ArticleParser(object):
    """
    Parsing HTML articles from Yahoo Finance.
    """

    def parse_native_yahoo(self, html):
        """Parse a native Yahoo finance article."""
        json_data = self._get_json_data(html)
        try:
            uuid = json_data['context']['dispatcher']['stores']['ContentStore']['uuidMap'].keys()[0]
            article_data = json_data['context']['dispatcher']['stores']['ContentStore']['uuidMap'][uuid]
        except TypeError, e:
            print str(e)
            return False
        # Parse text
        text, n_of_pars, n_of_words = self.__yahoo_parse_text(article_data['body'])
        author_name, author_title = self._get_author_from_json(article_data)
        # Result
        return {
            'text': text,
            'j_entities': article_data['entities'],
            'j_tags': article_data['tags'] if article_data['tags'] else None,
            'doc_type': article_data['type'],
            'author_name': author_name,
            'author_title': author_title,
            'yahoo_uuid': uuid,
            'article_body_data': json.dumps(article_data['body']),
            'paragraph_count': n_of_pars,
            'word_count': n_of_words,
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
            'paragraph_count': 1,
            'word_count': len(page_data['description'].split())
        }

    # PRIVATE METHODS

    def __yahoo_parse_text(self, a_body_data):
        """Edit article text to suitable format."""
        n_of_pars = 0
        n_of_words = 0
        a_text = ''
        for item in a_body_data:
            if item['type'] == 'text':
                i_soup = BeautifulSoup(item['content'], "lxml")
                if i_soup.style:
                    continue    # skip style tag
                i_text = i_soup.text.strip()
                if not i_text:
                    continue    # skip empty strings
                n_of_pars += 1
                n_of_words += len(i_text.split())
                a_text += '<p>%s</p>' % i_text
            if item['type'] == 'list':
                for x in item['listItems']:
                    i_soup = BeautifulSoup(x, "lxml")
                    i_text = i_soup.text.strip()
                    if not i_text:
                        continue
                    n_of_pars += 1
                    n_of_words += len(i_text.split())
                    a_text += '<p>%s</p>' % i_text
        # Remove all extra whitespace (single space remains).
        a_text = ' '.join(a_text.strip().split())
        # Result
        return a_text, n_of_pars, n_of_words

    def _get_json_data(self, text_file):
        app_data = None
        for line in text_file:
            if line.lstrip().startswith('root.App.main'):
                app_data = line[16:-2]
                break
        if app_data:
            return json.loads(app_data)
        else:
            raise AppDataNotFoundRetryException('JSON not found in article')

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

