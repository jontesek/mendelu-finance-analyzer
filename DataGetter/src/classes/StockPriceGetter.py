import urllib2
from datetime import datetime, timedelta

from StockPriceDbModel import StockPriceDbModel


class StockPriceGetter(object):

    def __init__(self):
        self.dbmodel = StockPriceDbModel()
        # full url: http://real-chart.finance.yahoo.com/table.csv?s=INTC&a=2&b=17&c=1980&d=9&e=3&f=2015&g=d&ignore=.csv
        self.price_url = 'http://real-chart.finance.yahoo.com/table.csv?s=%s&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=d&ignore=.csv'

    def get_prices_for_company_ticker(self, ticker, start_date, end_date):
        """
        :param ticker: string
        :param start_date: Date
        :param end_date: Date
        :return list
        """
        # First we must substract one month from the date, because the API is crazy.
        start_date = self._monthdelta(start_date, -1)
        end_date = self._monthdelta(end_date, -1)
        target_url = self.price_url % (ticker, start_date.month, start_date.day, start_date.year, end_date.month, end_date.day, end_date.year)
        # Get CSV file and turn it into list. Data in format: Date,Open,High,Low,Close,Volume,Adj Close
        try:
            data = urllib2.urlopen(target_url).read().split('\n')
        except Exception, e:
            print('not found: '+target_url)
            return False
        # remove first line (labels) and last line (empty)
        del(data[0])
        del(data[-1])
        # return list
        return data

    def save_prices_for_company(self, company_id, data):
        self.dbmodel.save_prices(company_id, data)

    def save_prices_for_all_companies(self, start_date, end_date):
        for comp in self.dbmodel.get_companies():
            data = self.get_prices_for_company_ticker(comp['ticker'], start_date, end_date)
            if data:
                self.save_prices_for_company(comp['id'], data)

    # or use: d2 = d - dateutil.relativedelta.relativedelta(months=1)
    def _monthdelta(self, date, delta):
        m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
        if not m: m = 12
        d = min(date.day, [31,
            29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
        return date.replace(day=d,month=m, year=y)