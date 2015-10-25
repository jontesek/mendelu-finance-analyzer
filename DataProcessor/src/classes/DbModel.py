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

