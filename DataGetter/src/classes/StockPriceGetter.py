import urllib2

from StockPriceDbModel import StockPriceDbModel


class StockPriceGetter(object):

    def __init__(self):
        self.dbmodel = StockPriceDbModel()
        # example: http://real-chart.finance.yahoo.com/table.csv?s=INTC&d=3&e=9&f=2016&g=d&a=2&b=17&c=1980&ignore=.csv
        self.price_url = 'http://real-chart.finance.yahoo.com/table.csv?s=%s&d=%d&e=%d&f=%d&g=d&a=%d&b=%d&c=%d&ignore=.csv'

    def get_prices_for_company_ticker(self, ticker, start_date, end_date):
        """
        :param ticker: string
        :param start_date: Date (The API has error - you must give the previous month.)
        :param end_date: Date
        :return list
        """
        # Build URL
        target_url = self.price_url % (ticker, end_date.month, end_date.day, end_date.year,
                                       start_date.month, start_date.day, start_date.year)
        print target_url
        # Get CSV file and turn it into list. Data in format: Date,Open,High,Low,Close,Volume,Adj Close
        try:
            data = urllib2.urlopen(target_url).read().split('\n')
        except Exception, e:
            print('not found: '+target_url)
            return False
        # Remove first line (labels) and last line (empty).
        del(data[0])
        del(data[-1])
        # Return list
        return data

    def save_prices_for_all_companies(self, start_date, end_date, stop_if_duplicate=True):
        print('>>>Saving stock prices from %s to %s') % (start_date, end_date)
        for comp in self.dbmodel.get_companies():
            data = self.get_prices_for_company_ticker(comp[1], start_date, end_date)
            if data:
                self.dbmodel.save_prices_for_company(comp[0], data, stop_if_duplicate)
        # the end
        print('>>>New stock prices were saved into DB.')
