from datetime import datetime
from classes.TextProcessor import TextProcessor


file_paths = {
    'stopwords': '../input_sources/google_en_stopwords.txt',
    'output_dir': 'C:/text_mining/data'
}
tp = TextProcessor(file_paths)
#from_date = datetime(2015, 8, 5)
from_date = datetime(2005, 5, 5)

delay = 1
company_id = 1

# Individual files
#tp.process_fb_posts_for_company(company_id, from_date, delay)
#tp.process_fb_comments_for_company(1, from_date, 1)
#tp.process_articles_for_company(1, from_date, 1)

# Total files
tp.process_all_fb_posts(from_date, delay)
# tp.process_all_fb_comments(from_date, delay)
#tp.process_all_articles(from_date, delay)
