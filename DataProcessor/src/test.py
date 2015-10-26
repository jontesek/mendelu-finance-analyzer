from datetime import datetime
from classes.TextProcessor import TextProcessor


file_paths = {'stopwords': '../input_sources/google_en_stopwords.txt'}
tp = TextProcessor(file_paths)
tp.set_stock_movements(1,datetime(2015,9,19))
tp.process_fb_posts_for_company(1,datetime(2015,9,20),1)
#tp.remove_stop_words('A zdar, from this shit')
#tp.process_fb_posts_for_company(1)





