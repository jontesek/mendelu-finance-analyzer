import datetime
from DbModel import DbModel


class StockPriceTransformer(object):

    def __init__(self):
        self.db_model = DbModel()

    def calculate_moving_average_for_company(self, company_id, period_length):
        """
        Calculate and save to DB simple moving average of close company price.
        :param company_id (int)
        :param period_length (int): in days
        :return:
        """
        # Get daily closing prices.
        min_date = datetime.date(1900, 1, 1)
        close_prices = self.db_model.get_stock_prices(company_id, min_date, 'close')
        # For first N-1 days just insert the close price.
        values = []
        for s_date, s_price in close_prices[0:period_length-1]:
            # self.db_model.update_stock_price(company_id, s_date, 'sma', s_price)
            values.append([company_id, s_date, s_price])
        # For remaining days calc the MA: (sum of current + previous n - 1 days) / period length
        for p_i, (s_date, s_price) in enumerate(close_prices[(period_length-1):], start=period_length-1):
            # Debug info
            #print p_i, (close_prices[(p_i - period_length + 1)][1]), s_price,
            # Save values
            previous_days_sum = sum([x[1] for x in close_prices[(p_i - period_length + 1):p_i]])
            total_sum = previous_days_sum + s_price
            mov_avg = total_sum / float(period_length)
            values.append([company_id, s_date, mov_avg])
        # Save values to DB.
        self.db_model.update_stock_prices_for_company('sma', values)

    def calculate_ma_for_all_companies(self, period_length):
        print('Calculating moving average for all companies.')
        for company in self.db_model.get_companies():
            print('MA for company %d') % company[0]
            self.calculate_moving_average_for_company(company[0], period_length)
        print('All companies prices updated.')
