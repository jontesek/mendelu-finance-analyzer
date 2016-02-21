from DbConnection import DbConnection


class DbModel(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.dbcon = DbConnection.get_con()

    def get_stock_prices(self, company_id, from_date="1970-01-01"):
        cursor = self.dbcon.cursor()
        query = 'SELECT date, close FROM stock_price WHERE company_id = %s AND date >= %s ORDER BY date ASC'
        cursor.execute(query, (company_id, from_date))
        return cursor.fetchall()

    def update_stock_price(self, company_id, price_date, field_name, field_value):
        cursor = self.dbcon.cursor()
        query = 'UPDATE stock_price SET %s = %s WHERE company_id = %s AND date = %s' % \
                (field_name, field_value, company_id, price_date)
        cursor.execute(query)
        #self.dbcon.commit()
        return cursor

    def update_stock_prices_for_company(self, field_name, values):
        cursor = self.dbcon.cursor()
        # Prepare query
        query = 'INSERT INTO stock_price (company_id, date, ' + field_name + ') VALUES (%s, %s, %s) '
        query += 'ON DUPLICATE KEY UPDATE ' + field_name + ' = VALUES(' + field_name + ')'
        # Execute query
        cursor.executemany(query, values)
        self.dbcon.commit()
        cursor.close()
