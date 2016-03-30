import sqlite3

conn = sqlite3.connect('scores.db')

conn.execute("DELETE FROM scores")

conn.commit()
conn.close()
