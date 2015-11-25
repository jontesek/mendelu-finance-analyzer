# -*- coding: utf-8 -*-
import re

text = """NEGATIVE
	NOT_GOOD
		@NOTGOOD [#POSITIVE_WORDS AFTER #NEGATIONS /S 3] (1)"""

text = "type=strongsubj len=1 word1=perva-sive pos1=adj stemmed1=n m priorpolarity=negative"
values = text.split(' ')
val_regex = re.compile('(.+)=(.+)')
val_regex.match(values[2]).group(2).strip()

text = "a	00003700	0.25	0	dissilient#1	bursting open with force, as do some ripe seed vessels"

text = "a	00002956	0	0.5	up_to#2 equal_to#1#1 abducent#1	especially of muscles; drawing away from the midline of the body or from an adjacent part"

values = text.split('\t')

pos_score = values[2]
neg_score = values[3]

terms = values[4].split(' ')
regexp_term = re.compile('(.+)#(\d+)')

term = regexp_term.match(terms[0]).group(1)
print term.replace('_',' ')

