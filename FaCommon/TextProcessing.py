import re


class TextProcessing(object):

    @staticmethod
    def process_facebook_text(text):
        # Remove hash tag symbols.
        text = text.replace('#', '')
        # Remove at symbols.
        text = text.replace('@', '')
        # Remove URL links.
        text = re.sub(r'https?://\S+', '', text)
        # Remove whitespace.
        text = ' '.join(text.strip().split())
        # Lowercase the text.
        text = text.lower()
        # Result
        return text

    @staticmethod
    def process_article_text(text):
        # Remove URL links.
        text = re.sub(r'https?://\S+', '', text)
        # Remove paragraph tags.
        text = re.sub(r'<p>|</p>', '', text)
        # Lowercase the text.
        text = text.lower()
        # Result
        return text
