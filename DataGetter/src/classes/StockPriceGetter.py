import urllib2
import datetime

from StockPriceDbModel import StockPriceDbModel


class StockPriceGetter(object):

    def __init__(self):
        self.dbmodel = StockPriceDbModel()
        # example: http://real-chart.finance.yahoo.com/table.csv?s=INTC&d=3&e=9&f=2016&g=d&a=2&b=17&c=2000&ignore=.csv
        self.price_url = 'http://real-chart.finance.yahoo.com/table.csv?s=%s&d=%d&e=%d&f=%d&g=d&a=%d&b=%d&c=%d&ignore=.csv'

    def get_prices_for_company_ticker(self, ticker, start_date, end_date):
        """
        :param ticker: string
        :param start_date: Date
        :param end_date: Date
        :return list
        """
        # The API has error - you must give the previous month.
        start_date = start_date - datetime.timedelta(days=33)
        # Build URL
        target_url = self.price_url % (ticker, end_date.month, end_date.day, end_date.year,
                                       start_date.month, start_date.day, start_date.year)
        print target_url
        # Get CSV file and turn it into list. Data in format: Date,Open,High,Low,Close,Volume,Adj Close
        try:
            data = urllib2.urlopen(target_url).read().split('\n')
        except Exception, e:
            print('not found: ' + target_url)
            return False
        # Remove first line (labels) and last line (empty).
        del(data[0])
        del(data[-1])
        # Return list
        return data

    def save_prices_for_all_companies(self, start_date, end_date, stop_if_duplicate=True, insert_missing_days=True):
        print('>>>Saving stock prices from %s to %s') % (start_date, end_date)
        for comp in self.dbmodel.get_companies():
            data = self.get_prices_for_company_ticker(comp[1], start_date, end_date)
            if data:
                if insert_missing_days:
                    new_data = self._refill_yahoo_data(comp[0], data, start_date, end_date)
                    self.dbmodel.save_refilled_prices_for_company(new_data)
                else:
                    self.dbmodel.save_prices_for_company(comp[0], data, stop_if_duplicate, insert_missing_days)
        # the end
        print('>>>New stock prices were saved into DB.')


    def _refill_yahoo_data(self, company_id, orig_yahoo_data, start_date, end_date):
        """
        For every missing day (i) from start to end date, insert artificial value: d_i = (d_i-1 + d_i+1)/2
        If yahoo date do not go to end_date, end function prematurely.

        :param company_id:
        :param orig_yahoo_data:
        :param start_date:
        :param end_date:
        :return:
        """
        # Prepare variables
        current_date = start_date
        plus_day = datetime.timedelta(days=1)
        y_last_day_i = 0
        all_days = []
        # Get last date from Yahoo.
        newest_yahoo_date = datetime.datetime.strptime(orig_yahoo_data[0].split(',')[0], '%Y-%m-%d').date()
        # Reverse data from oldest to newest.
        yahoo_data = list(reversed(orig_yahoo_data))
        # Loop all days from given interval.
        while current_date <= end_date:
            #print("==Examined date: %s") % current_date
            #print("Last yahoo date: %s") % yahoo_data[y_last_day_i][0:11]

            # Check if current date is not higher than the newest yahoo date.
            if current_date > newest_yahoo_date:
                break

            # Find the date in Yahoo data.
            for pr_i, price_str in enumerate(yahoo_data[y_last_day_i:], y_last_day_i):
                price_list = price_str.split(',')
                y_date = datetime.datetime.strptime(price_list[0], '%Y-%m-%d').date()
                # Skip too early dates.
                if y_date < start_date:
                    y_last_day_i = pr_i
                    continue
                # If the date was found, append it to new days.
                if current_date == y_date:
                    # Convert strings to floats.
                    floats_list = [float(x) for x in price_list[1:]]
                    # Create final data list.
                    f_day_list = [company_id, price_list[0]]
                    f_day_list.extend(floats_list)
                    # Save day data to all days.
                    all_days.append(f_day_list)
                    y_last_day_i = pr_i
                    #print("working date: %s") % (price_list[-1])
                    break
            # If the date was not found, calculate an artificial value for it.
            else:
                # Yahoo data row: date(0), open(1), high(2), low(3), close(4), volume(5), adjclose(6).
                d_close = self._calculate_new_var_value(yahoo_data, y_last_day_i, 4, 1)
                d_volume = self._calculate_new_var_value(yahoo_data, y_last_day_i, 5, 5)
                d_adjclose = self._calculate_new_var_value(yahoo_data, y_last_day_i, 6, 1)
                all_days.append([company_id, current_date, None, None, None, d_close, d_volume, d_adjclose])
                #print("non-working date: %s")  % d_adjclose

            # Either way, incerement date.
            current_date += plus_day

        # Result
        return all_days


    def _calculate_new_var_value(self, yahoo_data, last_day_i, var_pos_1, var_pos_2):
        date_list_1 = yahoo_data[last_day_i].split(',')
        date_list_2 = yahoo_data[last_day_i + 1].split(',')
        new_va1ue = (float(date_list_1[var_pos_1]) + float(date_list_2[var_pos_2])) / 2.0
        return new_va1ue

