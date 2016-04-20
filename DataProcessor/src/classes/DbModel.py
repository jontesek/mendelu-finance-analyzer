from DbConnection import DbConnection


class DbModel(object):

    def __init__(self):
        """Constructor"""
        self.dbcon = DbConnection.get_con()

    def get_companies(self):
        cursor = self.dbcon.cursor()
        query = 'SELECT id FROM COMPANY ORDER BY id ASC'
        cursor.execute(query)
        return cursor.fetchall()

    def get_stock_prices(self, company_id, from_date, price_type):
        cursor = self.dbcon.cursor()
        query = 'SELECT date, ' + price_type + ' FROM stock_price ' \
                                               'WHERE company_id = %s AND date >= %s ORDER BY date ASC'
        cursor.execute(query, (company_id, from_date))
        return cursor.fetchall()

    def update_stock_prices_for_company(self, field_name, values):
        cursor = self.dbcon.cursor()
        # Prepare query
        query = 'INSERT INTO stock_price (company_id, date, ' + field_name + ') VALUES (%s, %s, %s) '
        query += 'ON DUPLICATE KEY UPDATE ' + field_name + ' = VALUES(' + field_name + ')'
        # Execute query
        cursor.executemany(query, values)
        self.dbcon.commit()
        cursor.close()
