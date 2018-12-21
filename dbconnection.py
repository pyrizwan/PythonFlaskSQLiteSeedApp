import sqlite3

class dbconnection(object):
    def __init__(self):
        self.connection = None        

    def init_app(self, app):
        self.connection = sqlite3.connect('userdb.db')

    def close_connection(self):
        self.connection.close()

    def get_cursor(self):
        if not self.connection:
            raise RuntimeError('Attempt to get_cursor on uninitialized connection')
        return self.connection.cursor()

    def commit(self):
        if not self.connection:
            raise RuntimeError('Attempt to commit on uninitialized connection')
        return self.connection.commit()

sqlite_connection = dbconnection()