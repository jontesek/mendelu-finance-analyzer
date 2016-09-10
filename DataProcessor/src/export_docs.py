from datetime import datetime
import os
import itertools

from classes.DocumentsExporter import DocumentsExporter

#####
# PARAMETERS definition
####

# Prepare exporter object
file_paths = {
    'stopwords': '../input_sources/google_en_stopwords.txt',
    'output_dir': os.path.abspath('../../outputs/class_text/sma20_ewma5/fb_comment'),
}
d_exporter = DocumentsExporter(file_paths)
# Set lowest published date.
# Yahoo: 2014-06-18 21:24:00, twitter: 2014-11-20 09:32:02, fb post: 2009-04-15 17:10:55, fb commnent: 2009-04-16 13:51:28
#from_date = datetime(2000, 1, 1)

# Parameters lists
delays = [1, 2, 3]
price_types = ['adjclose', 'ewma', 'sma']
const_boundaries = [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5)]

# Create all combinations of parameters.
params_combinations = list(itertools.product(price_types, delays, const_boundaries))

#######
# EXECUTION
#######
#
# #### Process all Yahoo articles and Facebook posts.
# for (n_price_type, n_delay, n_boundary) in params_combinations:
#     print("======All companies: %s, %s, %s======") % (n_price_type, str(n_delay), str(n_boundary))
#     #d_exporter.process_documents_for_all_companies('article', from_date, n_delay, n_price_type, n_boundary, False, 50000, True)
#     #d_exporter.process_documents_for_all_companies('fb_post', from_date, n_delay, n_price_type, n_boundary, False, 100000, True)

#quit()

#### Process Facebook comments and tweets for one company.
# company_id = 48
# new_dir = os.path.abspath(d_exporter.file_paths['output_dir'] + '/sel_com')
# d_exporter.change_output_dir(new_dir)
#
# for (n_price_type, n_delay, n_boundary) in params_combinations:
#     print("===Company %d: %s, %s, %s===") % (company_id, n_price_type, str(n_delay), str(n_boundary))
#     #d_exporter.process_documents_for_company('tweet', company_id, from_date, n_delay, n_price_type, n_boundary, False)
#     print(d_exporter.process_documents_for_company('fb_comment', company_id, from_date, n_delay, n_price_type, n_boundary, False))

#### Process Facebook comments and tweets for multiple companies.
# Define companies
comp_ids_tw = [44, 202, 233, 300, 193, 58]
nonsearch_cids = [48, 217, 458, 479]
total_tw_ids = comp_ids_tw + nonsearch_cids
# Dates
from_date = datetime(2015, 8, 2).date()
to_date = datetime(2016, 4, 2).date()
# Set correct output directory.
# new_dir = os.path.abspath(d_exporter.file_paths['output_dir'] + '/fb_comment')
# d_exporter.change_output_dir(new_dir)
# Process all parameters and companies.
for (n_price_type, n_delay, n_boundary) in params_combinations:
    print("===Companies %s: %s, %s, %s===") % (str(total_tw_ids), n_price_type, str(n_delay), str(n_boundary))
    # d_exporter.process_documents_for_selected_companies(
    # total_tw_ids, 'tweet', from_date, to_date, n_delay, n_price_type, n_boundary, False, 1000000, False, nonsearch_cids)
    d_exporter.process_companies_by_source('all-fb-40pd', 'fb_comment', from_date, to_date, n_delay, n_price_type,
                                           n_boundary, False, 1000000)
