import sqlite3

conn = sqlite3.connect('restaurant.db')

if (conn):
    print('connection successful')
else:
    print('connection failed')