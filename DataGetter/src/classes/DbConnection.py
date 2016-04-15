import mysql.connector

import codecs
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)


class DbConnection(object):
    """
    Provides database connection for other classes.
    """
    dbcon = False

    @staticmethod
    def get_con():
        """
        Return an existing connection or create a new connection.
        :return: MySQLConnection
        """
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
