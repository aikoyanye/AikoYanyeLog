import sqlite3

db = sqlite3.connect('log.db')
cursor = db.cursor()
cursor.execute('SELECT * FROM title')
print(cursor.fetchall())