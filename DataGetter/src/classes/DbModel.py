from DbConnection import DbConnection


class DbModel(object):
    """
    Parent for classes working with DB.
    """

    def __init__(self):
        """
        Get a DB connection.
        """
        self.dbcon = DbConnection.get_con()

    def add_log_exec(self, script, exec_error):
        """
        Log execution of performing script and commit all changes to DB.
        :param script: int
        :param exec_error: boolean
        :return:
        """
        # Prepare variables
        err_v = 1 if exec_error else 0
        # Insert log 
        cursor = self.dbcon.cursor()
        query = "INSERT INTO log_exec (script, was_error) VALUES (%s, %s)"
        cursor.execute(query, (script, err_v))
        # Commit remaining queries
        self.dbcon.commit()
        cursor.close()
    