import sqlite3

sqlite_connection = sqlite3.connect('cart.db')
sqlite_create_table_query = '''CREATE TABLE cart (
                                id INTEGER PRIMARY KEY,
                                nickname TEXT NOT NULL,
                                cart TEXT,
                                passwd TEXT NOT NULL);'''

cursor = sqlite_connection.cursor()
print("База данных подключена к SQLite")
cursor.execute(sqlite_create_table_query)
sqlite_connection.commit()
print("Таблица SQLite создана")

cursor.close()
