import string
import nltk
import re

from libs.vaderSentiment.vader import SentimentIntensityAnalyzer as VaderAnalyzer
from LexiconReader import LexiconReader


class LexiconSentimentAnalyzer(object):

    NEUTRAL_S_LIMIT = (-0.05, 0.05)

    def __init__(self):
        self.lex_reader = LexiconReader()
        self.vader = VaderAnalyzer()

    def calculate_simple_sentiment(self, s_dictionary_name, input_text):
        """
        Calculate text sentiment in a simple way - sum of sentiments of all words in the text.

        Arguments:
            s_dictionary_name (string)
            input_text (string)

        Returns:
            float: sentiment value
        """
        # Get dictionary
        s_dict = self.lex_reader.get_dictionary(s_dictionary_name)
        # Tokenize text
        tokens = nltk.word_tokenize(input_text.lower())
        # Remove punctation
        tokens = [i for i in tokens if i not in string.punctuation]
        # Calculate sentiment
        sentiment_sum = 0
        found_tokens_count = 0.0
        for token in tokens:
            if token in s_dict:
                found_tokens_count += 1
                sentiment_sum += s_dict[token]
        # count percentage of found tokens
        percent_tokens_found = (found_tokens_count / len(tokens)) * 100
        # result
        return round(sentiment_sum, 3), round(percent_tokens_found, 3)

    def calculate_vader_sentiment(self, s_dictionary_name, input_text, split_sentences=False):
        """
        Calculate text sentiment using VADER algorithm and selected dictionary.

        Arguments:
            s_dictionary_name (string)
            input_text (string)

        Returns:
            float: sentiment value
        """
        # If necessary, reload VADER object.
        if s_dictionary_name != self.vader.lexicon_name:
            self.vader = VaderAnalyzer(s_dictionary_name)
            self.vader.lexicon_name = s_dictionary_name
            # test
            #print('reload')
            #print len(self.vader.lexicon.keys())
            #print self.vader.lexicon['}:-)']

        # Calculate sentiment for the whole text.
        if not split_sentences:
            return self.vader.polarity_scores(input_text)['compound']

        # If desired, split text into sentences.
        sentences = nltk.tokenize.sent_tokenize(input_text)
        # Calc sentiment for every sentence.
        sentiment_sum = 0.0
        for sent in sentences:
            values = self.vader.polarity_scores(sent)
            sentiment_sum += values['compound']
        # Calc sentiment for the whole text - normalize sum by number of sentences.
        return sentiment_sum / float(len(sentences))

    def format_sentiment_value(self, sent_value):
        """
        Return whether given sentiment value represents a positive, negative or neutral sentiment.
        :param sent_value (float):
        :return: string
        """
        if self.NEUTRAL_S_LIMIT[0] < sent_value < self.NEUTRAL_S_LIMIT[1]:
            polarity = 'neu'
        elif sent_value > 0:
            polarity = 'pos'
        elif sent_value < 0:
            polarity = 'neg'
        else:
            polarity = 'neu'
        return polarity

    def calculate_vader_sentiment_values(self, s_dictionary_name, input_text):
        """
        Calculate text sentiment using VADER algorithm and selected dictionary.
        Return compund value in form of sum and division.

        Arguments:
            s_dictionary_name (string)
            input_text (string)

        Returns:
            floats: compound sum, compound division
        """
        # If necessary, reload VADER object.
        if s_dictionary_name != self.vader.lexicon_name:
            self.vader = VaderAnalyzer(s_dictionary_name)
            self.vader.lexicon_name = s_dictionary_name
        # Split text into sentences.
        sentences = nltk.tokenize.sent_tokenize(input_text)
        # Calc sentiment for every sentence.
        sentiment_sum = 0.0
        for sent in sentences:
            values = self.vader.polarity_scores(sent)
            sentiment_sum += values['compound']
        # Calc sentiment for the whole text - normalize sum by number of sentences.
        sentiment_division = float(sentiment_sum / len(sentences))
        # result
        return sentiment_sum, round(sentiment_division, 4)
