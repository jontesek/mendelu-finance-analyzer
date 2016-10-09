import argparse
import json
import sys

from classes.LexiconSentimentAnalyzer import LexiconSentimentAnalyzer


sys.path.append('classes')

def get_sentiment(text, dictionary_name='custom_dict_orig'):
    """
    Get sentiment value of given text (using given dictionary).

    Args:
        text (str)
        dictionary_name (str):
            'custom_dict_orig' = VADER + financial terms
            'vader' = original VADER dictionary

    Returns:
        JSON string
        {
            'sentiment_no_split': float,        # Sentiment is calculated for the whole text.
            'sentiment_sentence_split': float,  # Text is splitted into sentences, sentiment is calculated for every sentence,
                                                # and the sum of sentiments is divided by number of sentences.
            'used_dict': str                    # Name of used sentiment dictionary.
        }
    """
    lsa = LexiconSentimentAnalyzer()
    value_no_split = lsa.calculate_vader_sentiment(dictionary_name, text, False)
    value_with_split = lsa.calculate_vader_sentiment(dictionary_name, text, True)

    return json.dumps({
        'sentiment_no_split': value_no_split,
        'sentiment_sentence_split': value_with_split,
        'used_dict': dictionary_name,
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for getting text's sentiment")
    parser.add_argument('--text', help='Text for which calculate sentiment')
    parser.add_argument('--dict', help='Which dictionary will be used', default='custom_dict_orig')

    args = parser.parse_args()
    result = get_sentiment(args.text, args.dict)
    print(result)
