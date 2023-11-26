import sqlite3 as sql

conn = sql.connect('phones.db')
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS phones(
               d_name text PRIMARY KEY,
               userid text PRIMATY KEY,
               number integer  
)""")

print ('DB and Table are created')

cursor.execute("""INSERT INTO phones VALUES(
               'SEP123412341234','imansur', '1234'
)""")


conn.commit()
cursor.close()

