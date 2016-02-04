from datetime import datetime
from classes.Exports import Exports

exp = Exports('../../outputs/exports')

company_id = 48
from_date = datetime(2015, 12, 1)

# Documents
exp.export_documents_for_company('fb_post', company_id, from_date)
exp.export_documents_for_company('fb_comment', company_id, from_date)
exp.export_documents_for_company('article', company_id, from_date)
exp.export_documents_for_company('tweet', company_id, from_date)

# Stock prices
exp.export_prices(company_id, from_date)
