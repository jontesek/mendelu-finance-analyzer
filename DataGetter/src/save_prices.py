from classes.StockPriceGetter import StockPriceGetter
import datetime

spg = StockPriceGetter()
#prices = spg.get_prices_for_company_ticker('INTC', datetime.date(2015, 3, 31), datetime.date(2015, 3, 31))
#spg.save_prices_for_company(233, prices)

# Prepare last date
last_date = datetime.datetime.now() - datetime.timedelta(days=1)

# Update prices
spg.save_prices_for_all_companies(datetime.date(2000, 1, 15), last_date.date(), True)
