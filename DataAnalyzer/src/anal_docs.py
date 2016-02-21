import time
import os.path

from classes.DocumentsAnalyzer import DocumentsAnalyzer

start_time = time.time()

output_dir = os.path.abspath('../../outputs')
da = DocumentsAnalyzer(output_dir, False)

#da.analyze_company(1, '2015-11-1', '2016-1-10', 'econom')
#da.analyze_company(217, '2016-1-1', '2016-1-14', 'econom-tw')
da.analyze_company(48, '2016-1-7', '2016-1-14', 'econom_att', 'close', True)
#da.analyze_all_companies('2016-01-05', '2016-01-10', 'stats_all')

#da.analyze_all_companies('2015-08-01', '2016-01-10', 'stats_all', 'close')

print("TOTAL RUNTIME:")
print("--- %s seconds ---" % (time.time() - start_time))
