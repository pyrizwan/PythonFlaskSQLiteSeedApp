import sqlite3

con = sqlite3.connect('userdb.db')

cursor = con.cursor()
cursor.execute("CREATE TABLE Users(Id INTEGER PRIMARY KEY, Username TEXT, Password TEXT, Firstname TEXT, Lastname TEXT)")

con.close()