import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('tokens.db')
cursor = conn.cursor()

# Создание таблиц
def create():
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_token (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        token TEXT UNIQUE,
                        status BOOLEAN NOT NULL,
                        admin BOOLEAN NOT NULL,
                        name TEXT,
                        user_id_telegram INTEGER
                   )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        number INTEGER,  -- Поле для номера заказа
                        pass TEXT,       -- Паспорт объекта
                        subsystem TEXT,  -- Подсистема объекта
                        address TEXT,    -- Адрес объекта
                        text TEXT,       -- Текстовый заказ
                        file BLOB,       -- Файлы, связанные с заказом
                        status TEXT NOT NULL, -- Статус заказа
                        user_id_telegram INTEGER -- ID пользователя в Telegram
                   )''')

    conn.commit()

# Вставка нового токена
def insert_user_token(token, status, admin, name):
    cursor.execute("""
            INSERT INTO user_token (token, status, admin, name)
            VALUES (?, ?, ?, ?)
        """, (token, status, admin, name))
    conn.commit()

# Вставка нового заказа
def insert_orders(pass_obj, text, file_blob, status, user_id_telegram):
    cursor.execute("""
            INSERT INTO orders (pass, text, file, status, user_id_telegram)
            VALUES (?, ?, ?, ?, ?)
        """, (pass_obj, text, file_blob, status, user_id_telegram))
    conn.commit()

# Показ всех токенов
def show_user_token():
    cursor.execute("SELECT * FROM user_token")
    data = cursor.fetchall()
    for row in data:
        print(row)

# Показ всех заказов
def show_orders():
    cursor.execute("SELECT * FROM orders")
    data = cursor.fetchall()
    for row in data:
        print(row)

# Удаление записи по ID в user_token
def delete_user_token(token_id):
    cursor.execute("DELETE FROM user_token WHERE id=?", (token_id,))
    conn.commit()

# Удаление записи по ID в orders
def delete_order(order_id):
    cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
    conn.commit()

# Функция для обновления таблицы orders, добавляя новые поля
def update_orders_table():
    try:
        # Добавляем поле number
        cursor.execute("ALTER TABLE orders ADD COLUMN number INTEGER")
    except sqlite3.OperationalError:
        print("Поле 'number' уже существует.")
    
    try:
        # Добавляем поле subsystem
        cursor.execute("ALTER TABLE orders ADD COLUMN subsystem TEXT")
    except sqlite3.OperationalError:
        print("Поле 'subsystem' уже существует.")
    
    try:
        # Добавляем поле address
        cursor.execute("ALTER TABLE orders ADD COLUMN address TEXT")
    except sqlite3.OperationalError:
        print("Поле 'address' уже существует.")
    
    # Применяем изменения
    conn.commit()

# Основной цикл программы с вводом данных
while True:
    a = input("0-exit\n1-create tables\n2-insert_user_token\n3-insert_orders\n4-show_user_token\n5-show_orders\n6-delete_user_token\n7-delete_order\n8-update_orders_table\n")
    
    if a == "0":
        break
    
    elif a == "1":
        create()
        print("Таблицы созданы (если они не существовали).")

    elif a == "2":
        # Ввод данных для нового токена
        token = input("Введите токен: ")
        status = input("Введите статус (0 или 1): ") == '1'
        admin = input("Администратор (0 или 1): ") == '1'
        name = input("Введите имя/описание токена: ")
        insert_user_token(token, status, admin, name)
        print("Токен успешно добавлен.")

    elif a == "3":
        # Ввод данных для нового заказа
        pass_obj = input("Введите паспорт объекта: ")
        text = input("Введите текст заказа: ")
        file_data = input("Введите путь к файлу (или пропустите): ")
        
        file_blob = None
        if file_data:
            with open(file_data, 'rb') as file:
                file_blob = file.read()
        
        status = input("Введите статус заказа: ")
        user_id_telegram = input("Введите ID пользователя Telegram (или пропустите): ")
        user_id_telegram = int(user_id_telegram) if user_id_telegram else None
        
        insert_orders(pass_obj, text, file_blob, status, user_id_telegram)
        print("Заказ успешно добавлен.")

    elif a == "4":
        show_user_token()

    elif a == "5":
        show_orders()

    elif a == "6":
        # Удаление токена по ID
        token_id = int(input("Введите ID токена для удаления: "))
        delete_user_token(token_id)
        print(f"Токен с ID {token_id} удален.")

    elif a == "7":
        # Удаление заказа по ID
        order_id = int(input("Введите ID заказа для удаления: "))
        delete_order(order_id)
        print(f"Заказ с ID {order_id} удален.")
    
    elif a == "8":
        # Обновление таблицы orders
        update_orders_table()
        print("Таблица orders обновлена.")

    else:
        print("Неверная команда, попробуйте снова.")

# Закрываем соединение с базой данных
conn.close()
