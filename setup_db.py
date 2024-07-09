import csv
import sqlite3

# Путь к вашему файлу CSV
csv_file = 'parsed_jobs.csv'

# Создание подключения к базе данных SQLite
conn = sqlite3.connect('vacan.db')
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vacan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT,
        company TEXT,
        description TEXT
    )
''')

# Создание таблицы для результатов
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vacan_result (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT,
        company TEXT,
        description TEXT
    )
''')

# Чтение данных из CSV и вставка их в таблицу
with open(csv_file, newline='', encoding='cp1251') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute('''
            INSERT INTO vacan (title, url, company, description)
            VALUES (?, ?, ?, ?)
        ''', (row['Название вакансии'], row['URL'], row['Название комании'], row['Описание']))

# Сохранение изменений и закрытие подключения
conn.commit()
conn.close()

print('Данные успешно загружены в базу данных.')
