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
#tp.process_documents_for_company('fb_post', company_id, from_date, delay)
#tp.process_documents_for_company('fb_comment', company_id, from_date, delay)
#tp.process_documents_for_company('article', company_id, from_date, delay)
#tp.process_documents_for_company('tweet', company_id, from_date, delay)

# Total files
#tp.process_documents_for_all_companies('fb_post', from_date, delay)
#tp.process_documents_for_all_companies('fb_comment', from_date, delay)
#tp.process_documents_for_all_companies('article', from_date, delay)
#tp.process_documents_for_all_companies('tweet', from_date, delay)
