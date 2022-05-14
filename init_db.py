import sqlite3

# python init_db.py

connection = sqlite3.connect('database.db') # file created when ran

# execute commands in SQL file that set up a database
with open('schema.sql') as file:
    connection.executescript(file.read())

connection.commit()
connection.close()
