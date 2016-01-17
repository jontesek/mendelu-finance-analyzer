import time

from classes.DocumentsAnalyzer import DocumentsAnalyzer

start_time = time.time()

da = DocumentsAnalyzer('../../outputs')
#da.analyze_company(1, '2015-11-1', '2016-1-14', 'econom')
#da.analyze_company(217, '2016-1-7', '2016-1-14', 'econom-tw')
da.analyze_all_companies('2015-08-1', '2016-1-14', 'econom-all')

print("TOTAL RUNTIME:")
print("--- %s seconds ---" % (time.time() - start_time))