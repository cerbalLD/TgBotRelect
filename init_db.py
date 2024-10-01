import sqlite3
conn = sqlite3.connect('tokens.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS user_token (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    token TEXT UNIQUE,
                    status BOOLEAN NOT NULL,
                    admin BOOLEAN NOT NULL,
                    name TEXT,
                    user_id_telegram INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pass TEXT,
                    text TEXT,
                    file BLOB,
                    status TEXT NOT NULL,
                    user_id_telegram INTEGER)''')
conn.commit()
conn.close()
print("База данных и таблицы успешно созданы.")
