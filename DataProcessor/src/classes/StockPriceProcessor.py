import datetime
from DbModel import DbModel


class StockPriceProcessor(object):

    def __init__(self):
        self.db_model = DbModel()
        self.stock_prices = {}

    def set_stock_prices(self, company_id, from_date, price_type='adjclose'):
        """
        Set stock prices for days from given date to present day.
        Must be called before calling get_price_movement method.

        Args:
            company_id (int): Company ID
            from_date (Date): from which date to search (also some previous days will be saved)
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
        # OK
        return True

    def _get_price_movement(self, first_date, second_date):
        """
        Get relative stock price movement: R_t = (P_t - P_t-1) / P_t-1

        Args:
            first_date (Date)
            second_date (Date)

        Returns:
            float: Stock price movement between the two dates (as percentage change).
        """
        ratio = (self.stock_prices[second_date] - self.stock_prices[first_date]) / self.stock_prices[first_date]
        #print first_date, second_date, ratio * 100, self.stock_prices[first_date], self.stock_prices[second_date]
        return ratio * 100

    def get_price_movement_with_delay(self, document_date, days_delay, const_boundaries):
        """
        Calculate direction of price movement with given delay and constant boundaries.

        Args:
            document_date (Date): When was document published.
            days_delay (int): How many days from published day should be reaction date.
            const_boundaries (list): [-A, +A] maximal value for contant state.

        Returns:
            string: const, up, down
        """
        # Create delayed date.
        reaction_date = document_date + datetime.timedelta(days=days_delay)
        # Calculate price movement.
        percentage_change = self._get_price_movement(document_date, reaction_date)
        #print percentage_change, const_boundaries, self._format_price_movement(percentage_change, const_boundaries)
        # Format movement to string.
        return self._format_price_movement(percentage_change, const_boundaries)

    def _format_price_movement(self, percentage_change, const_boundaries):
        """
        Get string representation of a size of stock movement.
        If the change is in interval (min, max), the movement is constant.
        If it's <= min and >= max, it's down and up, respectively.

        Args:
            percentage_change (float)
            const_boundaries (list): (min, max) interval for constant state

        Returns:
            string: const, up, down
        """
        if const_boundaries[0] < percentage_change < const_boundaries[1]:
            return 'const'
        if percentage_change > 0:
            return 'up'
        elif percentage_change < 0:
            return 'down'
        else:
            return 'const'

