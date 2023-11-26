import sqlite3 as sql

conn = sql.connect('phones.db')
cursor = conn.cursor()

d_name = ''
cursor.execute("SELECT d_name FROM phones") # query for specific column

data = ('SEP123412341264', 'kmansur', '1550')
add_command = "INSERT INTO phones VALUES {}".format(data)

existing_d_name = [row[0] for row in cursor.fetchall()]

if data[0] in existing_d_name:
    print ('This user already exists')
else:
    cursor.execute(add_command)
    conn.commit()
    cursor.close()

