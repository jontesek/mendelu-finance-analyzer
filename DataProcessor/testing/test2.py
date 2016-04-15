# -*- coding: utf-8 -*-
import re

# Facebook
text = '#Soldiers need defense equipment & #transportation they can count on. #LifeWith3M http://s.3m.com/bdwqw ahoj'
text2 = re.sub(r'#.+ ', '', text)
text3 = re.sub(r'www\..+\..+ ', '', text)
# Twitter
tweet = 'RT @BP_plc: #BP’s 2Q results. #Oil price. Deepwater Horizon. Bob Dudley discusses all in our interview: ' \
        'http://t.co/T7DLF0B8Fz http://t.co/…'
tweet2 = re.sub(r'@(\w+)', r'\1_xyzuser', tweet)
print tweet2



