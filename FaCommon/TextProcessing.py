import re


class TextProcessing(object):

    @staticmethod
    def process_facebook_text(text):
        # Remove whitespace
        text = ' '.join(text.strip().split())
        # Remove hyper links
        text = re.sub('https?:\/\/.* ?', '', text)
        # Remove hash tag symbols
        text = text.replace('#', '')
        # Lowercase the text
        text = text.lower()
        # result
        return text

    @staticmethod
    def process_article_text(text):
        # Remove whitespace
        text = ' '.join(text.strip().split())
        # Remove paragraph tags
        text = re.sub('<p>|</p>', '', text)
        # Lowercase the text
        text = text.lower()
        # result
        return text
