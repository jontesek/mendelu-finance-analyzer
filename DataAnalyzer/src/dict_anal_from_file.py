import time
import os.path
from datetime import datetime

from classes.DocumentsAnalyzer import DocumentsAnalyzer

####
# Parameter definitions.
####
output_dir = os.path.abspath('../../outputs/dict_anal_2')
da = DocumentsAnalyzer(output_dir, False)

price_type = 'adjclose'
c_dicts = ['custom_dict_orig', 'custom_dict_fs_added', 'custom_dict_only_fs']
const_boundaries = (-2, 2)

from_date = datetime(2015, 8, 2).date()
to_date = datetime(2016, 4, 2).date()

dict_name = c_dicts[2]
base_filename = '_' + price_type + '_' + dict_name.replace('_', '-')

####
# Testing part
####
# start_time = time.time()
# print("TOTAL RUNTIME:")
# print("--- %s seconds ---" % (time.time() - start_time))

da.analyze_company(1, from_date, to_date, 'comp1' + base_filename, price_type, const_boundaries, dict_name, True, 2)
#da.analyze_company(217, from_date, to_date, 'comp1' + base_filename, price_type, const_boundaries, dict_name, True)

#da.analyze_all_companies(from_date, to_date, 'daystats' + base_filename, 'sma', const_boundaries, dict_name)
exit()

####
# EXECUTION part
####

for d_name in c_dicts:
    base_filename = '_' + price_type + '_' + d_name.replace('_', '-')
    da.analyze_all_companies(from_date, to_date, 'daystats' + base_filename, price_type, const_boundaries, d_name, 2)

