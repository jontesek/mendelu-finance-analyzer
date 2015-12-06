import datetime
from DbModel import DbModel


class StockPriceProcessor(object):

    def __init__(self):
        self.db_model = DbModel()
        self.stock_movements = {'company_id': None, 'ratios': {}}
        self.const_boundaries = (-0.3, 0.3)

    def set_stock_movements(self, company_id, from_date):
        self.stock_movements = {'company_id': company_id, 'ratios': {}}
        """
        Get relative stock movement for days from given date to present day.

        Args:
            company_id (int): Company ID
            from_date (Datetime): from which date to search (also 3 previous days will be saved)

        Returns:
            list: (datetime, float): stock price movements as percentage change (current/last day)
        """
        # Substract 3 days to be sure to get data for the from_date.
        from_date = from_date.date()
        early_from_date = from_date - datetime.timedelta(days=3)
        # Get stock prices for individual dates
        stock_prices = self.db_model.get_stock_prices(company_id, early_from_date)
        # Create stock price movements for the dates
        for index, (price_date, price) in enumerate(stock_prices):
            if index == 0:
                continue
            ratio = (price / stock_prices[index - 1][1]) - 1
            self.stock_movements['ratios'][price_date] = ratio*100
        # result
        return self.stock_movements

    def create_lookup_and_find_working_date(self, doc_date, days_delay):
        lookup_date = doc_date + datetime.timedelta(days=days_delay)
        working_date = self._get_working_date(lookup_date)
        return working_date

    def get_stock_direction(self, working_date):
        price_movement = self.stock_movements['ratios'][working_date]
        movement_direction = self._format_stock_movement(price_movement, self.const_boundaries)
        return movement_direction

    def _format_stock_movement(self, percentage_change, const_boundaries):
        """
        Get string representation of a size of stock movement.

        :param percentage_change: percentage change
        :type float
        :param const_boundaries: [min, max] for constant state
        :return: direction
        """
        if const_boundaries[0] < percentage_change < const_boundaries[1]:
            return 'const'
        if percentage_change > 0:
            return 'up'
        elif percentage_change < 0:
            return 'down'
        else:
            return 'const'

    def _get_working_date(self, lookup_date):
        """
        Check if given date is a working day. If not, return minus one or minus two days date.

        Args:
            lookup_date (Datetime)

        Returns:
            Datetime: the same date or date of the previous working day
        """
        # For working day
        if lookup_date in self.stock_movements['ratios']:
            return lookup_date
        # Search past working date
        search_past_days = 14
        for i in range(1, search_past_days):
            date_minus = lookup_date - datetime.timedelta(days=i)
            if date_minus in self.stock_movements['ratios']:
                return date_minus
        # nothing found
        return False
