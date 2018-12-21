import sqlite3
#to use MySql database comment above line and uncomment below line
#import MySQLdb
class dbconnection(object):
    def __init__(self):
        self.connection = None        

    def init_app(self, app):
        self.connection = sqlite3.connect('userdb.db')
        #to use MySql database comment above line and uncomment below line
        #self.connection = MySQLdb.connect(host="localhost",user="root",passwd="",db="test") 

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

db_conn = dbconnection()