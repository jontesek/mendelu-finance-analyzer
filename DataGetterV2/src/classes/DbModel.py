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

    def add_log_exec(self, script_name, exec_error, start_time, end_time, duration_hours):
        """
        Log execution of performing script and commit all changes to DB.
        """
        # Prepare variables
        err_v = 1 if exec_error else 0
        # Insert log 
        cursor = self.dbcon.cursor()
        query = ("INSERT INTO log_exec (script_name, was_error, start_time, end_time, duration) "
                 "VALUES (%s, %s, %s, %s, %s)")
        cursor.execute(query, (script_name, err_v, start_time, end_time, duration_hours))
        # Commit remaining queries
        self.dbcon.commit()
        cursor.close()
