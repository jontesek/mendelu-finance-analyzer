import re

text = '#Soldiers need defense equipment & #transportation they can count on. #LifeWith3M http://s.3m.com/bdwqw ahoj'
text2 = re.sub(r'#.+ ', '', text)
text3 = re.sub(r'www\..+\..+ ', '', text)
print text2

num = 3
for i in range(1,3):
    print i

