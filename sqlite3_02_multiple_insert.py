import sqlite3 as sql

conn = sql.connect('phones.db')
cursor = conn.cursor()

phones = ['SEP123123123123','SEP142314231423', 'SEP987698769876']
users = ['imansur', 'amansur', 'emansur']
numbers = ['1010','1011','1012']

datas = list (zip(phones,users,numbers))

for data in datas :
    add_command = 'INSERT INTO phones VALUES {}'
    cursor.execute(add_command.format(data))
    print ('phone inserted')
conn.commit()
cursor.close()

