import sqlite3 as sql

conn = sql.connect('phones.db')
cursor = conn.cursor()

cursor.execute ("SELECT * FROM phones")
result = cursor.fetchone()              # Fetch one entery
result2 = cursor.fetchall()             # Fetch all entries

cursor.execute ("SELECT * FROM phones")
result3 = cursor.fetchmany(size=3)      # Fetch many entries tree row in example

cursor.execute ("SELECT number FROM phones")
result_num = cursor.fetchall()[1:]
for dn in result_num:
    print (dn[0])

