from datetime import datetime
import os

from classes.DocumentsExporter import DocumentsExporter


file_paths = {
    'stopwords': '../input_sources/google_en_stopwords.txt',
    #'output_dir': 'C:/text_mining/data/test',
    'output_dir': os.path.abspath('../../outputs/class_text/xtest'),
}
tp = DocumentsExporter(file_paths)
#from_date = datetime(2015, 8, 5)
from_date = datetime(2009, 1, 1)

delay = 2
company_id = 1

# Individual files
#tp.process_documents_for_company('fb_post', company_id, from_date, delay, 'close', (3, 3), False)
#tp.process_documents_for_company('fb_comment', company_id, from_date, delay, 'close')
#tp.process_documents_for_company('article', company_id, from_date, delay, 'adjclose', (-2, 2), False)
#tp.process_documents_for_company('tweet', company_id, from_date, delay, 'close')

c_ids = [44, 202, 233, 300]

for c_id in c_ids:
    print ('====COMPANY %s====') % c_id
    tp.process_daily_documents_for_company('tweet', c_id, datetime(2015, 8, 5).date(), datetime(2016, 4, 2).date(),
                                            delay, 'adjclose', (-3, 3), False, 25000)

# Total files
#tp.process_documents_for_all_companies('fb_post', from_date, delay, 'sma')
#tp.process_documents_for_all_companies('fb_comment', from_date, delay, 'close')
#tp.process_all_documents_for_all_companies('article', from_date, delay, 'close', (-3, 3), False, 30000)
#tp.process_documents_for_all_companies('tweet', from_date, delay, 'close')
exit()
# Bulk processing
price_type = 'sma'
for delay in [1, 2, 3]:
    print('>>>>>DELAY %d<<<<<') % delay
    #tp.process_documents_for_all_companies('fb_post', from_date, delay, price_type)
    tp.process_documents_for_all_companies('fb_comment', from_date, delay, price_type)
    #tp.process_documents_for_all_companies('article', from_date, delay, price_type)
    tp.process_documents_for_all_companies('tweet', from_date, delay, price_type)
