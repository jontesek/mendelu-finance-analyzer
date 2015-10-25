import mysql.connector

import codecs
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)


class DbConnection(object):
    """
    classdocs
    """
    dbcon = False

    def __init__(self):
        """
        Constructor
        """
    
    @staticmethod
    def get_con():
        if DbConnection.dbcon:
            return DbConnection.dbcon
        else:
            config = {
                'user': 'root',
                'password': 'autobus',
                'host': '127.0.0.1',
                'database': 'fin_analyzer',
                'charset': 'utf8mb4',
                'collation': 'utf8mb4_general_ci'
            }
            DbConnection.dbcon = mysql.connector.connect(**config)
            return DbConnection.dbcon