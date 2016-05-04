import time
import os.path
from datetime import datetime

from classes.DocumentsAnalyzer import DocumentsAnalyzer

####
# Parameter definitions.
####
output_dir = os.path.abspath('../../outputs/dict_anal')
da = DocumentsAnalyzer(output_dir, False)

price_type = 'adjclose'
dict_name = 'custom_dict_orig'
const_boundaries = (-2.5, 2.5)

from_date = datetime(2015, 8, 2).date()
to_date = datetime(2016, 4, 2).date()

base_filename = '_' + price_type + '_' + dict_name.replace('_', '-')

####
# Execution part.
####
start_time = time.time()

da.analyze_company(1, from_date, to_date, 'comp1' + base_filename, price_type, const_boundaries, dict_name, True)
#da.analyze_company(217, '2016-1-1', '2016-1-14', 'econom-tw')
#da.analyze_company(48, '2016-1-7', '2016-1-14', 'econom_att', 'close', True)
#da.analyze_all_companies('2016-01-05', '2016-01-10', 'stats_all')

#da.analyze_all_companies('2015-08-01', '2016-01-10', 'stats_sma', 'sma', const_boundaries, dict_name)


print("TOTAL RUNTIME:")
print("--- %s seconds ---" % (time.time() - start_time))
