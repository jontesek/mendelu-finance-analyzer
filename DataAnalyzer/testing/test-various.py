import nltk
import re
import string

comment = 'Hello, dear friend, this is not so cool :). oh man fuck this |-: oh yes.'

#print nltk.word_tokenize(comment)

print re.sub('[.]', '', comment).split()
