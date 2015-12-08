from classes.StockPriceGetter import StockPriceGetter
import datetime

spg = StockPriceGetter()
#prices = spg.get_prices_for_company_ticker('INTC', datetime.date(2015, 3, 31), datetime.date(2015, 3, 31))
#spg.save_prices_for_company(233, prices)

spg.save_prices_for_all_companies(datetime.date(2013, 10, 1), datetime.date(2015, 11, 1))

