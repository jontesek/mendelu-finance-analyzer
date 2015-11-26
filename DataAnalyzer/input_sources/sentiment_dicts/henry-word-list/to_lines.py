

# Read words
henry_file = open('negative.txt', 'r')

words = []
for line in henry_file:
	line_words = line.split(' ')
	words = words + line_words

# Write words
henry_file.close()
henry_file = open('negative_lines.txt', 'w+')
for word in words:
	henry_file.write(word.strip()+'\n')


