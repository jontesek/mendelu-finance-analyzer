import datetime

from classes.SimpleExporter import SimpleExporter


se = SimpleExporter('../../outputs/exports-vader', True)

company_id = 48
date_from = datetime.datetime(2000, 1, 1)
date_to = datetime.datetime(2016, 7, 13)

#se.analyze_company(company_id, date_from, date_to)

se.analyze_all_companies(date_from, date_to)
