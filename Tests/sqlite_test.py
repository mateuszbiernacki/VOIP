import sqlite3 as db

con = db.connect('example.db')
cur = con.cursor()
test = 'tableeeeee'
cur.execute('''CREATE TABLE :test
               (date text, trans text, symbol text, qty real, price real)''', {'test': test})
cur.execute("INSERT INTO :test VALUES ('2006-01-05','BUY','RHAT',100,35.14)", {'test': test})
con.commit()
for row in cur.execute('SELECT * FROM stocks ORDER BY price'):
        print(row)
con.close()
