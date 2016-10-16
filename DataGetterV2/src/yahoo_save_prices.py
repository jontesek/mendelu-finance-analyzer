import datetime
import os.path

from classes.StockPriceGetter import StockPriceGetter

spg = StockPriceGetter()

#prices = spg.get_prices_for_company_ticker('INTC', datetime.date(2016, 3, 31), datetime.date(2016, 5, 31))
#spg.save_prices_for_company(233, prices)

# Prepare last date
last_date = datetime.datetime.now() - datetime.timedelta(days=1)

# Update prices
spg.save_prices_for_all_companies(datetime.date(2008, 3, 3), last_date.date(), True, True)
