from mysql.connector.errors import IntegrityError
from DbModel import DbModel


class StockPriceDbModel(DbModel):


    ##### READ methods

    def get_companies(self):
        cursor = self.dbcon.cursor(dictionary=True)
        query = "SELECT id, ticker FROM company WHERE ticker IS NOT NULL ORDER BY id ASC"
        cursor.execute(query)
        return cursor.fetchall()


    #### WRITE methods

    def save_prices(self, company_id, data):
        cursor = self.dbcon.cursor()
        query = 'INSERT INTO stock_price (company_id,date,open,high,low,close,volume,adj_close) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        # Save prices for all days.
        for price_str in data:
            price_list = price_str.split(',')
            #price_list = [float(p) for p in price_list if ]
            price_list.insert(0, company_id)
            try:
                cursor.execute(query, price_list)
            except IntegrityError:
                continue
        # Save changes
        self.dbcon.commit()
        cursor.close()


