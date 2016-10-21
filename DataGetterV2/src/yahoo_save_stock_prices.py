import datetime
import os.path

from classes.StockPriceGetter import StockPriceGetter

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create the object
spg = StockPriceGetter()

#prices = spg.get_prices_for_company_ticker('INTC', datetime.date(2016, 3, 31), datetime.date(2016, 5, 31))
#spg.save_prices_for_company(233, prices)

# Prepare dates
#first_date = datetime.date(2008, 3, 3)
first_date = (datetime.datetime.now() - datetime.timedelta(days=35)).date()
last_date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()

# Update prices
start_time = datetime.datetime.now()
spg.save_prices_for_all_companies(first_date, last_date, True, True)
end_time = datetime.datetime.now()

# Log execution
script_name = os.path.basename(__file__).replace('.py', '')
duration = end_time - start_time
spg.db_model.add_log_exec(script_name, spg.exec_error, start_time, end_time, duration)
print('>>>>Script duration: {0}'.format(str(duration)))
