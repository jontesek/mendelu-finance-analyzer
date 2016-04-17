import datetime
from DbModel import DbModel


class StockPriceProcessor(object):

    def __init__(self):
        self.db_model = DbModel()
        self.stock_prices = {}

    def set_stock_prices(self, company_id, from_date, price_type='close'):
        """
        Set stock prices for days from given date to present day.
        Must be called before calling get_price_movement method.

        Args:
            company_id (int): Company ID
            from_date (Date): from which date to search (also some previous days will be saved)

        Returns:
            list: (Date, float): stock price movements as percentage change (current/last day)
        """
        self.stock_prices = {}
        # Substract some days to be sure to get data for the from_date.
        early_from_date = from_date - datetime.timedelta(days=7)
        # Get stock prices for individual dates.
        stock_prices = self.db_model.get_stock_prices(company_id, early_from_date, price_type)
        # Check if there was any result.
        if not stock_prices:
            return False
        # Create stock prices dictionary.
        for (price_date, price) in stock_prices:
            self.stock_prices[price_date] = price
        # Result
        return True

    def _get_price_movement(self, first_date, second_date):
        """
        Get relative stock price movement = second/first date.

        Args:
            first_date (Date)
            second_date (Date)
        Returns:
            float: stock price movement as percentage change
        """
        ratio = (self.stock_prices[second_date] / self.stock_prices[first_date]) - 1
        #print first_date, second_date, ratio*100
        return ratio*100

    def get_price_movement_with_delay(self, document_date, days_delay, const_boundaries):
        #print document_date
        # Get working days
        document_date = self._get_working_date(document_date, '-')
        if not document_date:
            return False
        reaction_date = document_date + datetime.timedelta(days=days_delay)
        reaction_date = self._get_working_date(reaction_date, '+')
        if not reaction_date:
            return False
        # Calculate price movement
        percent_change = self._get_price_movement(document_date, reaction_date)
        # Format movement to string
        return self._format_price_movement(percent_change, const_boundaries)

    def _format_price_movement(self, percentage_change, const_boundaries):
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

    def _get_working_date(self, lookup_date, direction):
        """
        Check if given date is a working day. If not, return plus/minus 1,2,..14 days date.

        Args:
            lookup_date (Datetime)

        Returns:
            Datetime: the same date or date of the previous working day
            False: If company was not on stock exchange.
        """
        # For working day
        if lookup_date in self.stock_prices:
            return lookup_date
        # Search future working date
        search_past_days = 14
        for i in range(1, search_past_days):
            if direction == '+':
                edited_date = lookup_date + datetime.timedelta(days=i)
            else:
                edited_date = lookup_date - datetime.timedelta(days=i)
            if edited_date in self.stock_prices:
                return edited_date
        # nothing found
        return False
