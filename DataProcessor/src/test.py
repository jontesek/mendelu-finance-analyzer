from datetime import datetime
from classes.TextProcessor import TextProcessor


file_paths = {
    'stopwords': '../input_sources/google_en_stopwords.txt',
    'output_dir': '../outputs'
}
tp = TextProcessor(file_paths)
# from_date = datetime(2015, 8, 5)
from_date = datetime(2005, 8, 5)
#tp.set_stock_movements(1, from_date)
#tp.process_fb_posts_for_company(1, from_date, 1)
tp.process_all_fb_posts(from_date, 1)

#tp.remove_stop_words('A zdar, from this shit')
#tp.process_fb_posts_for_company(1)
