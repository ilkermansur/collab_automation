import sqlite3 as sql

conn = sql.connect('phones.db')
cursor = conn.cursor()

phones = ['SEP123123123127','SEP142314231428', 'SEP987698769879']
users = ['pmansur', 'tmansur', 'hmansur']
numbers = ['1020','1021','1022']

datas = list (zip(phones,users,numbers))

cursor.executemany("INSERT INTO phones ('d_name','user_id','number') VALUES (?,?,?)", datas)

conn.commit()
cursor.close()

