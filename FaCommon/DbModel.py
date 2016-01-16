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

    def get_stock_prices(self, company_id, from_date):
        cursor = self.dbcon.cursor()
        query = 'SELECT date, close FROM stock_price WHERE company_id = %s AND date >= %s'
        cursor.execute(query, (company_id, from_date))
        return cursor.fetchall()
